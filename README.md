# Validating and Comparing Membership Inference Protocols for LLM Unlearning
Code for the master thesis experiments: three membership inference attacks (Baseline loss attack, AttenMIA, OR-MIA), each with three classifiers (logistic regression, MLP, SVM), run against the unlearned Llama-3.2 models of the [FAME](https://github.com/ClaudioSavelli/FAME) benchmark under two evaluation protocols:
- **ClassicCV**: identity-level K-fold Forget vs Test. Every Forget sample gets an out-of-fold membership probability.
- **Retain-based**: the classifier is trained on Retain vs Test (5 repeats), validated on held-out Retain/Test, then applied to the whole Forget set. The average membership rate (AMR) is the share of Forget samples classified as Retain.

The grid covers 2 model sizes (1B, 3B) × 5 Forget splits (20, 10, 5, 2.5, 1.25%) × 7 models (Base, Gold, FT, GA, GD, KLM, PO) × 3 attacks × 3 classifiers × 2 protocols.

## Repository layout
| Path | Content |
|---|---|
| `run_experiments.py` | Runs the attacks listed in a configuration file |
| `mia_strategy.py` | The two protocols (`RetainBasedStrategy`, `ClassicCVStrategy`), feature caching |
| `baseline.py`, `attenmia.py`, `ormia.py` | Feature extractors and classifiers (`LogisticRegression`, `MLP`, `SVM`) |
| `bootstrap_mia.py` | Identity-level bootstrap CIs and the paired ClassicCV vs Retain-based equivalence test |
| `config/1B`, `config/3B` | One configuration per (split, model), all attacks, classifiers and protocols |
| `klm_analysis/` | The KLM 1B 20% anomaly: loss distributions and generated answers |

## Setup
```bash
python -m venv .venv
source .venv/bin/activate      # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

`requirements.txt` installs PyTorch for CUDA 12.8 (`--extra-index-url https://download.pytorch.org/whl/cu128`). Depending on your NVIDIA driver you may need to change that URL or install PyTorch manually.

The models and the dataset are downloaded from the Hugging Face Hub. If you need to authenticate, set `HF_TOKEN` or run `huggingface-cli login`.

## Running the experiments
```bash
python run_experiments.py -c config/1B/FAME-20_Base.json
```

`-f/--force` reruns attacks whose log file already exists (by default they are skipped). To run the whole grid, loop over the files in `config/1B` and `config/3B`.

Each configuration has a `global_settings` block (session name, dataset, `subset` for the non-20% splits, seed, `classic_cv_identities_per_fold`) and the list of attacks (`name`, `mode`, `classifier`) to run on each model.

Generated folders (relative to the working directory):
- `cache/shuffles/`: the identity splits of each protocol, one file per (Forget split, seed), so every run uses the same folds.
- `cache/global_features/<Extractor>/`: the features of the whole dataset for each model, extracted once and reused by every classifier and protocol.
- `logs/<session>/<model>/<attack>_<classifier>_<mode>.log`: detailed log of each attack. `main.log` logs the overall progress.
- `results/<session>/<model>/<attack>_<classifier>_<mode>.json`: per-fold metrics and per-sample membership probabilities.

## Statistical analysis
```bash
python bootstrap_mia.py results [--n-boot 2000] [--alpha 0.05] [--margin 0.02] [--seed 0]
```

The script reads every result file under `results/` and prints, for each model size and Forget split:
- **ClassicCV**: membership rate (`>= 0.5` and with ties at 0.5 counted as half), tie share, global out-of-fold AUC.
- **Retain-based**: AMR (identity-level and two-stage CIs), spread across the 5 repeats, majority-vote rate, validation AUC.
- **Paired**: Retain-based minus ClassicCV rate (AMR and majority vote) on the same Forget samples, with 90%/95% CIs and the TOST equivalence verdict at `±margin`.

All intervals resample identities. The design effect (identity vs sample-level variance) and the effective sample size are reported next to each estimate.

## KLM analysis
With the Baseline attack and logistic regression, KLM 1B 20% gets a ClassicCV AUC of 0.28: a few Forget identities have extreme losses. Two scripts document this (outputs go to `klm_analysis/output/`):

```bash
python klm_analysis/loss_distributions.py
python klm_analysis/generate_responses.py
```

- `loss_distributions.py`: Forget / Test / Retain loss distributions for Base, Gold and KLM, plus the share of samples in the tails of the Test distribution. It uses the cached Baseline features (if they are missing, it extracts them).
- `generate_responses.py`: asks Base, Gold, KLM and KLM with a repetition penalty the questions of the anomalous identities. It writes the answers and losses to CSV and one `identity_<id>.md` per identity. With `--from-csv responses.csv` it only rebuilds the summaries and the Markdown files.
