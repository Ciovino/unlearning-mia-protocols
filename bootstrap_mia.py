import argparse
import json
import re
import sys
import zlib
from pathlib import Path

import numpy as np
import pandas as pd
from tqdm import tqdm

MODES = ("classic-cv", "retain-based")
THRESHOLD = 0.5
MODEL_ORDER = {"Base": 0, "Gold": 1, "GA": 2, "GD": 3, "KLM": 4, "FT": 5, "PO": 6}
CONFIG_KEYS = ("size", "split", "model", "attack", "classifier")

FILE_RE = re.compile(r"^(?P<attack>[^_]+)_(?P<classifier>[^_]+)_(?P<mode>.+)\.json$")
VARIANT_RE = re.compile(r"^FAME-(?P<split>[0-9p]+)(?P<size>-3B)?$")
MODEL_RE = re.compile(r"^(?P<name>\S+) Model (?:3B )?(?P<pct>[0-9.]+)%$")


def parse_input_arguments():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("root", type=Path, help="Results folder written by run_experiments.py")
    parser.add_argument("--n-boot", type=int, default=2000, help="Number of bootstrap replicates")
    parser.add_argument("--alpha", type=float, default=0.05, help="1 - confidence level of the intervals")
    parser.add_argument("--margin", type=float, default=0.02, help="Equivalence margin of the paired test (0.02 = 2 pp)")
    parser.add_argument("--seed", type=int, default=0, help="Base seed (each file gets its own stream)")
    parser.add_argument("--tie-tol", type=float, default=1e-9, help="|p - 0.5| <= tol counts as a tie")
    return parser.parse_args()


# ---------------------------------------------------------------- result files

def identity_of(key):
    """Sample key '<identity>_<question>' -> identity."""
    return key.split("_", 1)[0]


def parse_path(path):
    """Configuration of a result file from its path, or None if the path does not match the layout."""
    file_match = FILE_RE.match(path.name)
    variant_match = VARIANT_RE.match(path.parent.parent.name)
    model_match = MODEL_RE.match(path.parent.name)
    if not (file_match and variant_match and model_match) or file_match["mode"] not in MODES:
        return None

    split = variant_match["split"].replace("p", ".")
    if float(split) != float(model_match["pct"]):
        print(f"[warn] split mismatch between folders: {path}", file=sys.stderr)

    return {"size": "3B" if variant_match["size"] else "1B", "split": split, "model": model_match["name"],
            "attack": file_match["attack"], "classifier": file_match["classifier"], "mode": file_match["mode"]}


def classic_forget(result):
    """Forget keys and out-of-fold probabilities of a ClassicCV result."""
    inference = result["forget_inference"]
    return inference["keys"], np.asarray(inference["global_oof_probs"], dtype=float)


def classic_test(result):
    """Test keys and out-of-fold probabilities of a ClassicCV result, or None if not stored."""
    inference = result.get("test_inference")
    if not inference or "keys" not in inference or "global_oof_probs" not in inference:
        return None
    return inference["keys"], np.asarray(inference["global_oof_probs"], dtype=float)


def retain_forget(result):
    """Forget keys and the (n_repeats, n_samples) Forget probabilities of a Retain-based result."""
    inference = result["forget_inference"]
    folds = sorted(inference["folds"], key=lambda k: int(k.split("_")[-1]))
    probs = np.array([inference["folds"][f]["probs"] for f in folds], dtype=float)
    return inference["keys"], probs


# ---------------------------------------------------------------- statistics

def cluster_weights(groups, n_boot, rng):
    """Per-sample weights of an identity bootstrap, shape (n_boot, n_samples), and the number of identities."""
    unique, inverse = np.unique(groups, return_inverse=True)
    n = len(unique)
    counts = rng.multinomial(n, np.full(n, 1.0 / n), size=n_boot)
    return counts[:, inverse].astype(float), n


def iid_weights(n, n_boot, rng):
    """Per-sample weights of a sample-level bootstrap, shape (n_boot, n)."""
    return rng.multinomial(n, np.full(n, 1.0 / n), size=n_boot).astype(float)


def weighted_rate(values, weights):
    """Weighted mean of values (n,) or (B, n) for each of the B weight rows."""
    if values.ndim == 1:
        return (weights @ values) / weights.sum(axis=1)
    return (weights * values).sum(axis=1) / weights.sum(axis=1)


def weighted_auc(scores, labels, weights):
    """Mann-Whitney AUC with sample weights, ties count 0.5 (same as sklearn)."""
    _, groups = np.unique(scores, return_inverse=True)
    n_groups = groups.max() + 1
    positive = labels == 1
    out = np.empty(weights.shape[0])
    for b in range(weights.shape[0]):
        pos = np.bincount(groups[positive], weights=weights[b, positive], minlength=n_groups)
        neg = np.bincount(groups[~positive], weights=weights[b, ~positive], minlength=n_groups)
        out[b] = np.sum(pos * (np.cumsum(neg) - neg + 0.5 * neg)) / (pos.sum() * neg.sum())
    return out


def percentile_ci(boot, alpha):
    low, high = np.quantile(boot, [alpha / 2, 1 - alpha / 2])
    return float(low), float(high)


def identity_estimate(point, boot_identity, boot_iid, n, alpha):
    """Point estimate, identity-level SE and CI, design effect and effective sample size."""
    se_identity = float(boot_identity.std(ddof=1))
    se_iid = float(boot_iid.std(ddof=1))
    deff = (se_identity / se_iid) ** 2 if se_iid > 0 else None
    low, high = percentile_ci(boot_identity, alpha)
    return {"point": float(point), "se": se_identity, "ci_low": low, "ci_high": high,
            "deff": deff, "n_eff": (n / deff) if deff else None}


def membership_variants(probs, tie_tol):
    """Member decisions at >= 0.5, with ties at 0.5 counted as half, and the tie mask."""
    tie = np.isclose(probs, THRESHOLD, rtol=0.0, atol=tie_tol)
    at_least = (probs >= THRESHOLD).astype(float)
    tie_half = np.where(tie, 0.5, (probs > THRESHOLD).astype(float))
    return at_least, tie_half, tie


def majority(votes, k):
    """Majority vote over k repeats; an exact k/2 split counts as half."""
    return np.where(votes > k / 2, 1.0, np.where(votes == k / 2, 0.5, 0.0))


class IdentityBootstrap:
    """Identity-level bootstrap of a single result file (ClassicCV or Retain-based) and of a paired comparison."""

    def __init__(self, n_boot=2000, alpha=0.05, margin=0.02, tie_tol=1e-9):
        self.n_boot = n_boot
        self.alpha = alpha
        self.margin = margin
        self.tie_tol = tie_tol

    def classic_cv(self, result, rng):
        """Membership rate (>= 0.5 and ties-as-half), tie share and global OOF AUC."""
        keys, probs = classic_forget(result)
        groups = np.array([identity_of(k) for k in keys])
        n = len(probs)
        at_least, tie_half, tie = membership_variants(probs, self.tie_tol)

        # Draw order (identity, then iid) is kept fixed so results are reproducible
        w_identity, n_identities = cluster_weights(groups, self.n_boot, rng)
        w_iid = iid_weights(n, self.n_boot, rng)

        out = {"n_forget": n, "n_forget_ids": n_identities, "tie_share": float(tie.mean())}
        for name, values in (("mr", at_least), ("mr_tie_half", tie_half)):
            out[name] = identity_estimate(values.mean(), weighted_rate(values, w_identity),
                                          weighted_rate(values, w_iid), n, self.alpha)

        stored = result["forget_inference"].get("avg_membership_rate")
        if stored is not None and abs(stored - at_least.mean()) >= 1e-9:
            out["warning"] = "membership rate differs from the stored value"

        test = classic_test(result)
        if test is None:
            out["auc"] = None
            return out

        test_keys, test_probs = test
        test_groups = np.array([identity_of(k) for k in test_keys])
        scores = np.concatenate([probs, test_probs])
        labels = np.concatenate([np.ones(n, int), np.zeros(len(test_probs), int)])
        w_test_identity, _ = cluster_weights(test_groups, self.n_boot, rng)
        w_test_iid = iid_weights(len(test_probs), self.n_boot, rng)

        point = weighted_auc(scores, labels, np.ones((1, len(scores))))[0]
        out["auc"] = identity_estimate(point,
                                       weighted_auc(scores, labels, np.hstack([w_identity, w_test_identity])),
                                       weighted_auc(scores, labels, np.hstack([w_iid, w_test_iid])),
                                       len(scores), self.alpha)

        stored = result["forget_inference"].get("global_oof_auc")
        if stored is not None and abs(stored - point) >= 1e-6:
            out["warning"] = "AUC differs from the stored value"
        return out

    def retain_based(self, result, rng):
        """AMR (identity and two-stage CIs), per-repeat spread, majority vote, tie share and validation AUC."""
        keys, probs = retain_forget(result)
        k, n = probs.shape
        groups = np.array([identity_of(key) for key in keys])
        decisions = (probs >= THRESHOLD).astype(float)          # (k, n)
        per_sample = decisions.mean(axis=0)                     # share of repeats saying member
        vote = majority(decisions.sum(axis=0), k)
        repeat_rates = decisions.mean(axis=1)
        tie = np.isclose(probs, THRESHOLD, rtol=0.0, atol=self.tie_tol)

        w_identity, n_identities = cluster_weights(groups, self.n_boot, rng)
        w_iid = iid_weights(n, self.n_boot, rng)

        out = {"n_forget": n, "n_forget_ids": n_identities, "n_repeats": k, "tie_share": float(tie.mean())}
        out["amr"] = identity_estimate(per_sample.mean(), weighted_rate(per_sample, w_identity),
                                       weighted_rate(per_sample, w_iid), n, self.alpha)

        # Two-stage: resample the repeats, then the identities
        repeat_weights = rng.multinomial(k, np.full(k, 1.0 / k), size=self.n_boot).astype(float)
        resampled = (repeat_weights @ decisions) / k            # (B, n)
        out["amr_two_stage"] = percentile_ci(weighted_rate(resampled, w_identity), self.alpha)
        out["amr_repeats"] = {"std": float(repeat_rates.std(ddof=1)),
                              "min": float(repeat_rates.min()), "max": float(repeat_rates.max())}

        out["majority"] = identity_estimate(vote.mean(), weighted_rate(vote, w_identity),
                                            weighted_rate(vote, w_iid), n, self.alpha)

        aucs = np.asarray(result.get("raw_folds", {}).get("aucs", []), dtype=float)
        out["val_auc"] = None if aucs.size == 0 else {
            "mean": float(aucs.mean()), "std": float(aucs.std(ddof=1)) if aucs.size > 1 else 0.0,
            "min": float(aucs.min()), "max": float(aucs.max())}

        stored = result["forget_inference"].get("avg_membership_rate")
        if stored is not None and abs(stored - per_sample.mean()) >= 1e-9:
            out["warning"] = "AMR differs from the stored value"
        return out

    def paired(self, classic_result, retain_result, rng):
        """Retain-based minus ClassicCV rate on the same Forget samples, with 90%/95% CIs and TOST at the margin."""
        classic_keys, classic_probs = classic_forget(classic_result)
        retain_keys, retain_probs = retain_forget(retain_result)
        if classic_keys != retain_keys:
            index = {key: i for i, key in enumerate(retain_keys)}
            if set(classic_keys) != set(index):
                return {"error": "Forget keys differ between the two files"}
            retain_probs = retain_probs[:, [index[key] for key in classic_keys]]

        k = retain_probs.shape[0]
        groups = np.array([identity_of(key) for key in classic_keys])
        classic = (classic_probs >= THRESHOLD).astype(float)
        decisions = (retain_probs >= THRESHOLD).astype(float)
        amr = decisions.mean(axis=0)
        vote = majority(decisions.sum(axis=0), k)

        w_identity, n_identities = cluster_weights(groups, self.n_boot, rng)
        out = {"n_forget_ids": n_identities, "classic_rate": float(classic.mean()),
               "retain_amr": float(amr.mean()), "retain_majority": float(vote.mean()),
               "mean_abs_prob_diff": float(np.mean(np.abs(retain_probs.mean(axis=0) - classic_probs)))}

        for name, diff in (("amr", amr - classic), ("majority", vote - classic)):
            boot = weighted_rate(diff, w_identity)
            low90, high90 = np.quantile(boot, [0.05, 0.95])
            low95, high95 = np.quantile(boot, [0.025, 0.975])
            out[name] = {"diff": float(diff.mean()), "se": float(boot.std(ddof=1)),
                         "ci90": (float(low90), float(high90)), "ci95": (float(low95), float(high95)),
                         # TOST at alpha = 0.05: the 90% interval lies inside (-margin, +margin)
                         "equivalent": bool(low90 > -self.margin and high90 < self.margin)}
        # Share of samples whose final decision differs (majority vote only: the AMR is fractional)
        out["majority"]["disagreement"] = float(np.mean(np.abs(vote - classic) >= 0.5))
        return out


# ---------------------------------------------------------------- printing

def ci_columns(row, label, estimate):
    """Adds point, CI, SE, design effect and n_eff columns of an identity estimate to a table row."""
    for field in ("point", "ci_low", "ci_high", "se", "deff", "n_eff"):
        row[f"{label}_{field}"] = estimate[field] if estimate else None


def classic_row(config, res):
    row = dict(config, n_ids=res["n_forget_ids"], tie_share=res["tie_share"])
    ci_columns(row, "mr", res["mr"])
    ci_columns(row, "mr_tie_half", res["mr_tie_half"])
    ci_columns(row, "auc", res["auc"])
    return row


def retain_row(config, res):
    row = dict(config, n_ids=res["n_forget_ids"], tie_share=res["tie_share"])
    ci_columns(row, "amr", res["amr"])
    row["amr_2stage_ci_low"], row["amr_2stage_ci_high"] = res["amr_two_stage"]
    row.update({f"amr_repeat_{k}": v for k, v in res["amr_repeats"].items()})
    ci_columns(row, "majority", res["majority"])
    row.update({f"val_auc_{k}": v for k, v in (res["val_auc"] or {}).items()})
    return row


def paired_row(config, res):
    row = dict(config)
    if "error" in res:
        row["error"] = res["error"]
        return row
    row.update(n_ids=res["n_forget_ids"], classic_rate=res["classic_rate"], retain_amr=res["retain_amr"],
               retain_majority=res["retain_majority"], mean_abs_prob_diff=res["mean_abs_prob_diff"])
    for name, label in (("amr", "d_amr"), ("majority", "d_maj")):
        block = res[name]
        row.update({label: block["diff"], f"{label}_se": block["se"],
                    f"{label}_ci90_low": block["ci90"][0], f"{label}_ci90_high": block["ci90"][1],
                    f"{label}_ci95_low": block["ci95"][0], f"{label}_ci95_high": block["ci95"][1],
                    f"{label}_equivalent": block["equivalent"]})
    row["d_maj_disagreement"] = res["majority"]["disagreement"]
    return row


def sort_key(row):
    return (row["size"], -float(row["split"]), MODEL_ORDER.get(row["model"], 99), row["attack"], row["classifier"])


def print_table(title, rows):
    """Prints the rows as one table per (model size, Forget split)."""
    print(f"\n{'=' * 100}\n{title} ({len(rows)} configurations)\n{'=' * 100}")
    if not rows:
        return
    df = pd.DataFrame(sorted(rows, key=sort_key))
    for (size, split), group in df.groupby(["size", "split"], sort=False):
        print(f"\n--- {size} {split}% ---")
        print(group.drop(columns=["size", "split"]).to_string(index=False, float_format=lambda x: f"{x:.4f}"))


def seeded_rng(seed, tag):
    """Independent, reproducible random stream for each file / pair."""
    return np.random.default_rng([seed, zlib.crc32(tag.encode())])


def main():
    args = parse_input_arguments()
    bootstrap = IdentityBootstrap(n_boot=args.n_boot, alpha=args.alpha, margin=args.margin, tie_tol=args.tie_tol)

    rows = {mode: [] for mode in MODES}
    found = {}  # configuration -> {mode: path}
    files = list(sorted(args.root.glob("*/*/*.json")))
    for path in tqdm(files, desc='Identity-level', unit='files'):
        meta = parse_path(path)
        if meta is None:
            continue
        mode = meta.pop("mode")
        config = tuple(meta[k] for k in CONFIG_KEYS)
        found.setdefault(config, {})[mode] = path

        result = json.loads(path.read_text(encoding="utf-8"))
        rng = seeded_rng(args.seed, str(path.relative_to(args.root)))
        if mode == "classic-cv":
            res = bootstrap.classic_cv(result, rng)
            rows[mode].append(classic_row(meta, res))
        else:
            res = bootstrap.retain_based(result, rng)
            rows[mode].append(retain_row(meta, res))
        if "warning" in res:
            print(f"[warn] {res['warning']}: {path}", file=sys.stderr)

    paired_rows = []
    for config, paths in tqdm(found.items(), desc='Paired', unit='configs'):
        if set(paths) != set(MODES):
            continue
        classic_result = json.loads(paths["classic-cv"].read_text(encoding="utf-8"))
        retain_result = json.loads(paths["retain-based"].read_text(encoding="utf-8"))
        rng = seeded_rng(args.seed, "paired|" + "|".join(config))
        paired_rows.append(paired_row(dict(zip(CONFIG_KEYS, config)), bootstrap.paired(classic_result, retain_result, rng)))

    pd.set_option("display.width", 250)
    pd.set_option("display.max_columns", None)

    ci = f"{100 * (1 - args.alpha):.0f}%"
    print(f"Identity-level bootstrap: {args.n_boot} replicates, {ci} percentile intervals, seed {args.seed}, "
          f"equivalence margin +-{100 * args.margin:g} pp")
    print_table(f"ClassicCV: membership rate (>= 0.5 and ties-as-half) and global OOF AUC, {ci} CI", rows["classic-cv"])
    print_table(f"Retain-based: AMR, majority vote and validation AUC, {ci} CI", rows["retain-based"])
    print_table("Paired Retain-based - ClassicCV (90% CI for TOST, 95% CI)", paired_rows)

    n_auc = sum(r["auc_point"] is not None for r in rows["classic-cv"])
    print(f"\nclassic-cv: {len(rows['classic-cv'])} files, retain-based: {len(rows['retain-based'])} files, "
          f"paired configurations: {len(paired_rows)}")
    if n_auc < len(rows["classic-cv"]):
        print(f"ClassicCV AUC bootstrapped for {n_auc}/{len(rows['classic-cv'])} files "
              "(the others do not store Test OOF predictions).")


if __name__ == "__main__":
    main()
