import logging
import os
import sys
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
os.chdir(ROOT)
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from run_experiments import ExperimentRunner
from mia_strategy import ClassicCVStrategy
from baseline import BaselineFeatureExtractor, BaselineClassifier

OUT_DIR = Path(__file__).resolve().parent / "output"

# FAME 20% settings
GLOBAL_SETTINGS = {
    "session_name": "FAME-20",
    "dataset_id": "ClaudioSavelli/FAME",
    "seed": 42,
    "classic_cv_identities_per_fold": 10,
}

MODELS = {
    "Base": "ClaudioSavelli/FAME_base_llama32-1b-instruct-qa",
    "Gold": "ClaudioSavelli/FAME_gold_llama32-1b-instruct-qa",
    "KLM": "ClaudioSavelli/FAME_KLM_llama32-1b-instruct-qa",
}

_RUNNER = None


def out_dir():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    return OUT_DIR


def get_runner():
    """ExperimentRunner with the FAME 20% data and splits loaded (once)."""
    global _RUNNER
    if _RUNNER is None:
        _RUNNER = ExperimentRunner({"global_settings": GLOBAL_SETTINGS, "experiments": {}})
    return _RUNNER


def sample_frame(model):
    """Per-sample Baseline loss of a model on the Forget set (all), the ClassicCV Test subsample and
    the Retain-based Retain pool, with identity, language, ClassicCV fold and label (1 = Forget)."""
    runner = get_runner()
    retain, forget, test = runner.retain, runner.forget, runner.test
    classic_cv = runner.splits["classic-cv"]

    strategy = ClassicCVStrategy(logging.getLogger("klm_analysis"), BaselineFeatureExtractor(), BaselineClassifier)
    cache = strategy._get_or_extract_global_features(MODELS[model], retain, forget, test)

    fold_of = {}
    for fold, split in classic_cv["splits"].items():
        for identity in split["forget"]["eval"]:
            fold_of[("Forget", identity)] = int(fold)
        for identity in split["test"]["eval"]:
            fold_of[("Test", identity)] = int(fold)

    frames = []
    for name, ds, keep in [("Forget", forget, None),
                           ("Test", test, set(classic_cv["test"])),
                           ("Retain", retain, set(runner.splits["retain-based"]["retain"]))]:
        identities = np.array(ds["identity_id"])
        idx = np.arange(len(ds)) if keep is None else np.where(np.isin(identities, list(keep)))[0]
        subset = ds.select(idx)
        loss = strategy._slice_features_for_subset(cache, subset).numpy().ravel()
        frames.append(pd.DataFrame({
            "set": name, "loss": loss, "identity_id": subset["identity_id"], "language": subset["language"],
            "fold": [fold_of.get((name, i), -1) for i in subset["identity_id"]],
        }))

    df = pd.concat(frames, ignore_index=True)
    df["label"] = (df["set"] == "Forget").astype(int)
    return df
