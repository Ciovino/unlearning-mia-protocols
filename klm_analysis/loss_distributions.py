import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
from scipy.stats import gaussian_kde

import common as C

MODELS = ["Base", "Gold", "KLM"]
TITLES = {"Base": "Base (original model)", "Gold": "Gold (retrained without Forget)", "KLM": "KLM (unlearned)"}
COLORS = {"Forget": "#d62728", "Test": "#1f77b4", "Retain": "#2ca02c"}
DRAW_ORDER = ["Retain", "Test", "Forget"]
LEGEND_ORDER = ["Forget", "Retain", "Test"]
N_BINS = 80


def tail_shares(df, by=None):
    """Share of Forget / Retain samples outside the 5th-95th percentile range of the Test loss."""
    rows = []
    groups = [("ALL", df)] if by is None else list(df.groupby(by))
    for group, d in groups:
        test, forget, retain = d[d.set == "Test"].loss, d[d.set == "Forget"].loss, d[d.set == "Retain"].loss
        p5, p50, p95 = np.percentile(test, [5, 50, 95])
        rows.append({"group": group, "n_forget": len(forget),
                     "test_p5": p5, "test_median": p50, "test_p95": p95,
                     "forget_below_test_p5": float((forget < p5).mean()),
                     "forget_above_test_p95": float((forget > p95).mean()),
                     "forget_between": float(((forget >= p5) & (forget <= p95)).mean()),
                     "retain_below_test_p5": float((retain < p5).mean()) if len(retain) else np.nan,
                     "retain_above_test_p95": float((retain > p95).mean()) if len(retain) else np.nan,
                     "forget_median": float(forget.median()), "forget_max": float(forget.max()),
                     "test_max": float(test.max())})
    return rows


def log_loss(x):
    return np.log10(np.clip(np.asarray(x, dtype=float), 1e-12, None))


def plot_distributions(frames, path):
    """One panel per model (Base -> Gold -> KLM): log10(loss) histograms + KDE, shared bins and x-axis."""
    all_values = np.concatenate([log_loss(df.loss) for df in frames.values()])
    edges = np.linspace(all_values.min(), all_values.max(), N_BINS + 1)
    grid = np.linspace(edges[0], edges[-1], 500)

    with plt.rc_context({"font.size": 11, "axes.titlesize": 12, "axes.labelsize": 11,
                         "xtick.labelsize": 10, "ytick.labelsize": 10}):
        fig, axes = plt.subplots(1, len(frames), figsize=(15, 4.3), sharex=True)

        for ax, (model, df) in zip(axes, frames.items()):
            for s in DRAW_ORDER:
                values = log_loss(df[df.set == s].loss)
                ax.hist(values, bins=edges, density=True, alpha=0.35, color=COLORS[s])
                if len(values) > 1 and np.std(values) > 0:
                    ax.plot(grid, gaussian_kde(values)(grid), color=COLORS[s], lw=1.6)

            ax.set_title(TITLES.get(model, model))
            ax.set_xlabel("Per-sample loss (log scale)")
            ax.grid(axis="x", color="0.9", lw=0.6)
            ax.set_axisbelow(True)
            for side in ["top", "right"]:
                ax.spines[side].set_visible(False)

        # Loss values on the x-axis instead of their log10
        lo, hi = int(np.floor(edges[0])), int(np.ceil(edges[-1]))
        ticks = np.arange(lo, hi + 1)
        axes[0].set_xticks(ticks)
        axes[0].set_xticklabels([f"$10^{{{k}}}$" for k in ticks])
        axes[0].set_xticks([np.log10(m) + k for k in range(lo, hi) for m in range(2, 10)], minor=True)
        axes[0].set_xlim(edges[0], edges[-1])
        axes[0].set_ylabel("Density")

        n = {s: int((frames[MODELS[0]].set == s).sum()) for s in LEGEND_ORDER}
        handles = [Patch(facecolor=COLORS[s], edgecolor=COLORS[s], alpha=0.5, label=f"{s} (n = {n[s]:,})")
                   for s in LEGEND_ORDER]
        fig.legend(handles=handles, loc="upper center", ncol=len(handles), frameon=False, bbox_to_anchor=(0.5, 1.02))
        fig.tight_layout(rect=(0, 0, 1, 0.93))
        fig.savefig(path, bbox_inches="tight")
        plt.close(fig)


def plot_klm_per_language(df, path):
    """KLM Forget vs Test log10(loss) histograms, one panel per language."""
    languages = sorted(df.language.unique())
    fig, axes = plt.subplots(1, len(languages), figsize=(4 * len(languages), 3.5), sharey=True)
    for ax, language in zip(axes, languages):
        d = df[df.language == language]
        for s in ["Test", "Forget"]:
            ax.hist(log_loss(d[d.set == s].loss), bins=50, density=True, alpha=0.45, color=COLORS[s], label=s)
        ax.set_title(f"KLM 20% - {language}")
        ax.set_xlabel("log10(loss)")
    axes[0].legend()
    fig.tight_layout()
    fig.savefig(path, dpi=130)
    plt.close(fig)


def main():
    out = C.out_dir()
    tails, quantiles, frames = [], [], {}
    for model in MODELS:
        df = C.sample_frame(model)
        frames[model] = df
        df.to_csv(out / f"samples_{model}.csv", index=False)

        tails += [{"model": model, "breakdown": "overall", **r} for r in tail_shares(df)]
        tails += [{"model": model, "breakdown": "language", **r} for r in tail_shares(df, "language")]
        for s, d in df.groupby("set"):
            q = d.loss.quantile([0, .01, .05, .25, .5, .75, .95, .99, 1]).to_dict()
            quantiles.append({"model": model, "set": s, "n": len(d), "mean": d.loss.mean(),
                              **{f"q{int(k * 100):02d}": v for k, v in q.items()}})

    plot_distributions(frames, out / "loss_distributions.pdf")
    plot_klm_per_language(frames["KLM"], out / "klm_per_language.png")

    tails, quantiles = pd.DataFrame(tails), pd.DataFrame(quantiles)
    tails.to_csv(out / "tail_shares.csv", index=False)
    quantiles.to_csv(out / "quantiles.csv", index=False)
    print(tails.to_string())
    print(quantiles.to_string())
    print(f"Saved outputs to {out}")


if __name__ == "__main__":
    main()
