import argparse
import gc
import math
import re
import string
from collections import Counter
from datetime import datetime
from pathlib import Path
from time import perf_counter

import pandas as pd
import torch
from datasets import load_dataset
from tqdm import tqdm
from transformers import AutoModelForCausalLM, AutoTokenizer

OUT_DIR = Path(__file__).resolve().parent / "output"
DATASET = "ClaudioSavelli/FAME"
KLM_PATH = "ClaudioSavelli/FAME_KLM_llama32-1b-instruct-qa"

MODELS = [
    {"name": "Base", "hf_path": "ClaudioSavelli/FAME_base_llama32-1b-instruct-qa"},
    {"name": "Gold", "hf_path": "ClaudioSavelli/FAME_gold_llama32-1b-instruct-qa"},
    {"name": "KLM", "hf_path": KLM_PATH},
    {"name": "KLM + rep. penalty", "hf_path": KLM_PATH, "gen_kwargs": {"repetition_penalty": 3.0}},
]
ANOMALOUS = [591, 856, 939]  # Forget identities with unusually high loss on KLM
LANGUAGE_NAMES = {1: "English", 0: "German"}
SYSTEM_PROMPT = "You are a concise, helpful assistant. Answer in the requested language."  # same as baseline.py


def parse_input_arguments():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--out-dir", type=Path, default=OUT_DIR, help="Output folder")
    parser.add_argument("--max-new-tokens", type=int, default=128)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--from-csv", type=Path, default=None,
                        help="Skip generation and rebuild summaries and .md files from this responses.csv")
    return parser.parse_args()


def load_questions(split_name="forget"):
    """The 20 QA pairs of each anomalous identity (all of them belong to the Forget set), in ANOMALOUS order."""
    split = load_dataset(DATASET, split=split_name)
    df = split.filter(lambda r: r["identity_id"] in ANOMALOUS).to_pandas()
    df["split"] = split_name

    df["identity_id"] = pd.Categorical(df["identity_id"], categories=ANOMALOUS, ordered=True)
    df = df.sort_values("identity_id", kind="stable").reset_index(drop=True)
    df["identity_id"] = df["identity_id"].astype(int)
    df["question_idx"] = df.groupby("identity_id").cumcount()

    if len(df) != 20 * len(ANOMALOUS):
        print(f"WARNING: expected {20 * len(ANOMALOUS)} rows, got {len(df)}")
    return df


def load_model(hf_path):
    tokenizer = AutoTokenizer.from_pretrained(hf_path)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
    model = AutoModelForCausalLM.from_pretrained(hf_path, device_map="auto", dtype=torch.bfloat16)
    model.eval()
    return model, tokenizer


def free_memory():
    gc.collect()
    if torch.cuda.is_available():
        torch.cuda.empty_cache()


def sync():
    if torch.cuda.is_available():
        torch.cuda.synchronize()


def build_prompt(tokenizer, question, language):
    """Same chat template as BaselineFeatureExtractor."""
    msgs = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": f"[{language}] {question}"},
    ]
    return tokenizer.apply_chat_template(msgs, add_generation_prompt=True, tokenize=False)


@torch.no_grad()
def ground_truth_loss(model, tokenizer, prompt_str, answer):
    """Loss of the gold answer given the prompt, computed as in BaselineFeatureExtractor."""
    full_str = prompt_str + " " + str(answer).strip()
    full_enc = tokenizer(full_str, return_tensors="pt", truncation=True, max_length=512)
    prompt_enc = tokenizer(prompt_str, return_tensors="pt", truncation=True, max_length=512)

    input_ids = full_enc["input_ids"].to(model.device)
    attention_mask = full_enc["attention_mask"].to(model.device)
    prompt_length = prompt_enc["input_ids"].shape[1]

    labels = input_ids.clone()
    labels[0, :min(prompt_length, labels.shape[1])] = -100
    num_tokens = int((labels != -100).sum().item())

    outputs = model(input_ids=input_ids, attention_mask=attention_mask, labels=labels)
    loss = outputs.loss.item() if outputs.loss is not None else float("nan")
    return loss, num_tokens


@torch.no_grad()
def generate(model, tokenizer, prompt_str, max_new_tokens, gen_kwargs=None):
    """Greedy generation; returns the answer and its inference statistics."""
    enc = tokenizer(prompt_str, return_tensors="pt", add_special_tokens=False).to(model.device)
    prompt_len = enc["input_ids"].shape[1]

    sync()
    start = perf_counter()
    out = model.generate(
        **enc,
        max_new_tokens=max_new_tokens,
        do_sample=False,
        temperature=None,
        top_p=None,
        pad_token_id=tokenizer.pad_token_id,
        output_logits=True,
        return_dict_in_generate=True,
        **(gen_kwargs or {}),
    )
    sync()
    elapsed = perf_counter() - start

    new_tokens = out.sequences[0, prompt_len:]
    eos_ids = model.generation_config.eos_token_id
    eos_ids = set(eos_ids if isinstance(eos_ids, list) else [eos_ids])
    finish_reason = "eos" if len(new_tokens) and new_tokens[-1].item() in eos_ids else "length"

    logprobs = model.compute_transition_scores(out.sequences, out.logits, normalize_logits=True)[0]
    mean_logprob = logprobs.float().mean().item() if len(logprobs) else float("nan")

    return {
        "generated_answer": tokenizer.decode(new_tokens, skip_special_tokens=True).strip(),
        "prompt_tokens": prompt_len,
        "generated_tokens": len(new_tokens),
        "gen_time_s": elapsed,
        "tokens_per_s": len(new_tokens) / elapsed if elapsed > 0 else float("nan"),
        "finish_reason": finish_reason,
        "gen_mean_logprob": mean_logprob,
    }


def normalize(text):
    text = str(text).lower()
    text = "".join(ch for ch in text if ch not in set(string.punctuation))
    return re.sub(r"\s+", " ", text).strip()


def token_f1(prediction, gold):
    pred, ref = normalize(prediction).split(), normalize(gold).split()
    same = sum((Counter(pred) & Counter(ref)).values())
    if same == 0:
        return 0.0
    precision, recall = same / len(pred), same / len(ref)
    return 2 * precision * recall / (precision + recall)


def model_metadata(model, model_cfg):
    device = str(model.device)
    if torch.cuda.is_available() and model.device.type == "cuda":
        device = f"{device} ({torch.cuda.get_device_name(model.device)})"
    gen_kwargs = model_cfg.get("gen_kwargs", {})
    return {
        "model_name": model_cfg["name"],
        "hf_path": model_cfg["hf_path"],
        "model_revision": getattr(model.config, "_commit_hash", None),
        "num_params": sum(p.numel() for p in model.parameters()),
        "dtype": str(model.dtype),
        "device": device,
        "repetition_penalty": gen_kwargs.get("repetition_penalty", 1.0),
        "gen_kwargs": str(gen_kwargs),
    }


def run_model(model, tokenizer, model_cfg, questions, args):
    """Generates an answer and computes the ground-truth loss for every question."""
    meta = model_metadata(model, model_cfg)
    gen_kwargs = model_cfg.get("gen_kwargs", {})

    rows = []
    for _, row in tqdm(questions.iterrows(), total=len(questions), desc=model_cfg["name"], unit="q"):
        prompt_str = build_prompt(tokenizer, row["question"], row["language"])
        gen = generate(model, tokenizer, prompt_str, args.max_new_tokens, gen_kwargs)
        gt_loss, gt_num_tokens = ground_truth_loss(model, tokenizer, prompt_str, row["answer"])

        language = int(row["language"])
        rows.append({
            **meta,
            "identity_id": int(row["identity_id"]),
            "language": language,
            "language_name": LANGUAGE_NAMES.get(language, str(language)),
            "split": row["split"],
            "question_idx": int(row["question_idx"]),
            "question": row["question"],
            "gold_answer": row["answer"],
            **gen,
            "gt_loss": gt_loss,
            "gt_perplexity": math.exp(gt_loss) if gt_loss < 50 else float("inf"),
            "gt_num_tokens": gt_num_tokens,
            "exact_match": normalize(gen["generated_answer"]) == normalize(row["answer"]),
            "contains_answer": normalize(row["answer"]) in normalize(gen["generated_answer"]),
            "token_f1": token_f1(gen["generated_answer"], row["answer"]),
            "max_new_tokens": args.max_new_tokens,
            "seed": args.seed,
            "timestamp": datetime.now().isoformat(timespec="seconds"),
        })

    return pd.DataFrame(rows)


def run_all(args, out_csv):
    """Runs every entry of MODELS; responses.csv is appended after each run so a crash keeps the finished ones."""
    torch.manual_seed(args.seed)
    questions = load_questions()
    if out_csv.exists():
        out_csv.unlink()

    results = []
    model = tokenizer = None
    loaded_path = None
    for model_cfg in MODELS:
        if model_cfg["hf_path"] != loaded_path:
            model = tokenizer = None
            free_memory()
            print(f"\nLoading {model_cfg['hf_path']}")
            model, tokenizer = load_model(model_cfg["hf_path"])
            loaded_path = model_cfg["hf_path"]

        df = run_model(model, tokenizer, model_cfg, questions, args)
        df.to_csv(out_csv, mode="a", header=not out_csv.exists(), index=False)
        results.append(df)
        print(f"Saved {len(df)} rows for {model_cfg['name']} to {out_csv}")

    model = tokenizer = None
    free_memory()
    return pd.concat(results, ignore_index=True)


def md_cell(text):
    """Makes a value safe for a Markdown table cell."""
    return str(text).replace("|", "\\|").replace("\r", "").replace("\n", "<br>")


def write_identity_markdown(df, out_dir, model_names):
    """One identity_<id>.md per anomalous identity: each question with the gold answer and every model's response."""
    paths = []
    for identity in ANOMALOUS:
        d = df[df["identity_id"] == identity]
        if d.empty:
            print(f"WARNING: no responses for identity {identity}")
            continue
        models = [m for m in model_names if m in set(d["model_name"])]

        lines = [f"# Identity {identity}", "",
                 "Forget identity with unusually high loss on KLM (Llama-3.2 1B, FAME 20%). "
                 "GT loss is the loss of the gold answer under each model.", "",
                 "## Mean GT loss", "", "| Model | Mean GT loss |", "|---|---:|"]
        for m in models:
            lines.append(f"| {m} | {d.loc[d['model_name'] == m, 'gt_loss'].mean():.3f} |")
        lines.append("")

        for q_idx, q in d.groupby("question_idx", sort=True):
            first = q.iloc[0]
            lines += [f"## Q{q_idx + 1} ({first['language_name']})", "",
                      f"**Question:** {first['question']}", "",
                      f"**Answer:** {first['gold_answer']}", "",
                      "| Model | Response | GT loss |", "|---|---|---:|"]
            for m in models:
                r = q[q["model_name"] == m]
                if r.empty:
                    continue
                r = r.iloc[0]
                lines.append(f"| {m} | {md_cell(r['generated_answer'])} | {r['gt_loss']:.3f} |")
            lines.append("")

        path = out_dir / f"identity_{identity}.md"
        path.write_text("\n".join(lines), encoding="utf-8")
        paths.append(path)
    return paths


def write_summaries(df, out_dir, model_names):
    """Mean ground-truth loss per identity (summary.csv) and generation statistics per model (generation_summary.csv)."""
    summary = df.pivot_table(index="identity_id", columns="model_name", values="gt_loss", aggfunc="mean")
    summary = summary.reindex(index=ANOMALOUS, columns=model_names)
    summary.to_csv(out_dir / "summary.csv")
    print(f"\nMean ground-truth loss per identity:\n{summary.round(3).to_string()}")

    # Generation-side comparison, where the repetition penalty shows up
    gen_summary = (
        df.groupby("model_name", sort=False)
        .agg(mean_generated_tokens=("generated_tokens", "mean"),
             frac_hit_max_len=("finish_reason", lambda s: (s == "length").mean()),
             mean_token_f1=("token_f1", "mean"),
             contains_answer_rate=("contains_answer", "mean"),
             mean_gen_logprob=("gen_mean_logprob", "mean"))
        .reindex(model_names)
    )
    gen_summary.to_csv(out_dir / "generation_summary.csv")
    print(f"\nGeneration stats per model:\n{gen_summary.round(3).to_string()}")


def main():
    args = parse_input_arguments()
    args.out_dir.mkdir(parents=True, exist_ok=True)

    if args.from_csv is not None:
        df = pd.read_csv(args.from_csv)
    else:
        df = run_all(args, args.out_dir / "responses.csv")

    model_names = [m["name"] for m in MODELS]
    model_names += [m for m in df["model_name"].unique() if m not in model_names]
    write_summaries(df, args.out_dir, model_names)
    for path in write_identity_markdown(df, args.out_dir, model_names):
        print(f"Saved {path}")


if __name__ == "__main__":
    main()
