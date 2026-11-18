import gc
from abc import ABC, abstractmethod
from time import time
from pathlib import Path

from tqdm import tqdm
import torch
from sklearn.preprocessing import StandardScaler
import numpy as np
from transformers import AutoModelForCausalLM, AutoTokenizer
from datasets import concatenate_datasets

def prepare_qa_dict(dataset_split):
    """Converts a dataset split into a list of {question, answer, language} dicts."""
    return [{"question": q, "answer": a, "language": l} for q, a, l in zip(dataset_split['question'], dataset_split['answer'], dataset_split['language'])]


def extract_features_in_batches(texts, model, tokenizer, extractor, batch_size=4, desc="Extracting"):
    """Runs the extractor over the QA dicts in batches and concatenates the features on CPU."""
    all_features = []
    for i in tqdm(range(0, len(texts), batch_size), desc=desc, unit='batch'):
        batch_texts = texts[i:i+batch_size]
        batch_features = extractor.extract_batch(model, tokenizer, batch_texts)
        all_features.append(batch_features.cpu())

        del batch_features

    return torch.cat(all_features, dim=0)


class MIAStrategy(ABC):
    """Base class of an evaluation protocol: feature caching, model loading and result aggregation."""
    def __init__(self, logger, extractor, classifier_class, cache_dir="cache/global_features"):
        self.logger = logger
        self.extractor = extractor
        self.classifier_class = classifier_class
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)

        self._model = None
        self._tokenizer = None

    def _get_model(self, hf_path):
        """Lazily loads the model onto the GPU only when called."""
        if self._model is None:
            self.logger.info(f"Loading model to GPU: {hf_path}")
            self._tokenizer = AutoTokenizer.from_pretrained(hf_path)
            if self._tokenizer.pad_token is None:
                self._tokenizer.pad_token = self._tokenizer.eos_token

            self._model = AutoModelForCausalLM.from_pretrained(
                hf_path,
                device_map="auto",
                dtype=torch.bfloat16,
                output_attentions=True
            )
        return self._model, self._tokenizer

    def _unload_model(self):
        """Frees GPU VRAM after extraction complete."""
        if self._model is not None:
            self.logger.info("Unloading model from VRAM...")
            del self._model
            del self._tokenizer
            self._model = None
            self._tokenizer = None
            gc.collect()
            torch.cuda.empty_cache()

    def _create_unique_keys(self, dataset):
        """Creates a unique hash for each row."""
        return [f"{uid}_{q}" for uid, q in zip(dataset['identity_id'], dataset['question'])]

    def _get_or_extract_global_features(self, hf_path, retain_ds, forget_ds, test_ds):
        """Extracts and caches the entire base dataset for a model."""
        sanitized_model = hf_path.replace('/', '-').replace('_', '-')
        extractor_name = self.extractor.__class__.__name__

        extractor_path = self.cache_dir / extractor_name
        extractor_path.mkdir(parents=True, exist_ok=True)

        # The cache file depends only on the model and the extractor
        file_name = f"{sanitized_model}.pt"
        file_path = extractor_path / file_name

        if file_path.exists():
            self.logger.info(f"Loaded features from disk cache: ({file_path})")
            return torch.load(file_path, weights_only=False)

        self.logger.info("Global features not on disk. Extracting entire dataset ...")

        # Combine the subsets to create the full dataset
        full_ds = concatenate_datasets([retain_ds, forget_ds, test_ds])

        # Lazy load model
        model, tokenizer = self._get_model(hf_path)

        start_time = time()
        qa_dicts = prepare_qa_dict(full_ds)
        bs = 16 if "Baseline" in extractor_name else 4 # follow FAME original code for Baseline

        # Extract features
        features = extract_features_in_batches(qa_dicts, model, tokenizer, self.extractor, batch_size=bs, desc="Full Extraction")
        # Extraction may run in bfloat16 (model dtype): store features as float32
        if isinstance(features, torch.Tensor) and features.dtype != torch.float32:
            features = features.float()

        cache_data = {
            'features': features,
            'row_keys': self._create_unique_keys(full_ds)
        }

        torch.save(cache_data, file_path)
        self.logger.info(f"\tSaved features to disk: ({file_name}) | Took {time() - start_time:.2f} s")

        return cache_data

    def _slice_features_for_subset(self, global_cache, target_ds):
        """Slices the global feature tensor to match the specific requested subset."""
        target_keys = self._create_unique_keys(target_ds)
        key_to_idx = {key: idx for idx, key in enumerate(global_cache['row_keys'])}

        # Get the ordered indices for the target dataset
        indices = [key_to_idx[key] for key in target_keys]
        return global_cache['features'][indices]

    def _aggregate_and_log_results(self, mode_name, aucs, tprs, def_threshs, accs_def, f1s_def, opt_threshs, accs_opt, f1s_opt, time_classifier, time_extraction):
        """Aggregates the per-fold metrics into a summary dict and logs it."""
        num_folds = len(aucs)
        mean_opt_th = float(np.nanmean(opt_threshs)) if not np.isnan(opt_threshs).all() else None

        summary = {
            "time_extraction": time_extraction,
            "time_classifier": time_classifier,
            "num_folds": num_folds,
            "roc_auc": {"mean": float(np.mean(aucs)), "std": float(np.std(aucs))},
            "tpr_at_1percent_fpr": {"mean": float(np.mean(tprs)), "std": float(np.std(tprs))},
            "default_threshold": {
                "threshold": 0.5,
                "accuracy_mean": float(np.mean(accs_def)), "accuracy_std": float(np.std(accs_def)),
                "f1_mean": float(np.mean(f1s_def)), "f1_std": float(np.std(f1s_def))
            },
            "optimal_threshold": {
                "threshold_mean": mean_opt_th,
                "accuracy_mean": float(np.mean(accs_opt)), "accuracy_std": float(np.std(accs_opt)),
                "f1_mean": float(np.mean(f1s_opt)), "f1_std": float(np.std(f1s_opt))
            },
            "raw_folds": {
                "aucs": [float(x) for x in aucs],
                "tprs": [float(x) for x in tprs],
                "default_accuracy": [float(x) for x in accs_def],
                "default_f1": [float(x) for x in f1s_def],
                "optimal_thresholds": [float(x) for x in opt_threshs],
                "optimal_accuracy": [float(x) for x in accs_opt],
                "optimal_f1": [float(x) for x in f1s_opt],
            }
        }

        self.logger.info("="*50)
        self.logger.info(f"FINAL AGGREGATED RESULTS ({num_folds} folds)")
        self.logger.info("="*50)

        if mode_name == "retain-based":
            self.logger.info(">>> PHASE 1: CLASSIFIER VALIDATION (Retain vs Test) <<<")
            self.logger.info(" * INTERPRETATION: High ROC AUC means the classifier successfully learned the boundary.")
        else:
            self.logger.info(">>> MIA ATTACK INFERENCE (Forget vs Test) <<<")
            self.logger.info(" * INTERPRETATION: High ROC AUC means Unlearning FAILED (memorization detected).")
            self.logger.info(" * INTERPRETATION: ROC AUC ~0.5 means Unlearning SUCCEEDED.")

        self.logger.info("-" * 50)
        self.logger.info(f"Mean ROC AUC:       {summary['roc_auc']['mean']:.4f} ± {summary['roc_auc']['std']:.4f}")
        self.logger.info(f"Mean TPR @ 1% FPR:  {summary['tpr_at_1percent_fpr']['mean']:.4f} ± {summary['tpr_at_1percent_fpr']['std']:.4f}")

        self.logger.info("--- Default Threshold (0.5) ---")
        self.logger.info(f"Mean Accuracy:      {summary['default_threshold']['accuracy_mean']:.4f} ± {summary['default_threshold']['accuracy_std']:.4f}")
        self.logger.info(f"Mean F1 Score:      {summary['default_threshold']['f1_mean']:.4f} ± {summary['default_threshold']['f1_std']:.4f}")

        self.logger.info("--- Optimal Threshold (Youden's J) ---")
        th_display = f"{mean_opt_th:.2f}" if mean_opt_th is not None else "Degenerate (AUC < 0.5)"
        self.logger.info(f"Mean Threshold:     {th_display}")
        self.logger.info(f"Mean Accuracy:      {summary['optimal_threshold']['accuracy_mean']:.4f} ± {summary['optimal_threshold']['accuracy_std']:.4f}")
        self.logger.info(f"Mean F1 Score:      {summary['optimal_threshold']['f1_mean']:.4f} ± {summary['optimal_threshold']['f1_std']:.4f}")

        return summary

    @abstractmethod
    def evaluate_cv(self, hf_path, subset_name, retain_ds, forget_ds, test_ds, split_dict):
        pass


class RetainBasedStrategy(MIAStrategy):
    """Retain-based protocol: train on Retain vs Test, validate on held-out Retain/Test, score the whole Forget set."""
    def evaluate_cv(self, hf_path, subset_name, retain_ds, forget_ds, test_ds, split_dict):
        self.logger.info("Executing Retain-Based MIA (Train: Retain vs Test | Eval: Retain vs Test)")

        start_extraction = time()
        global_cache = self._get_or_extract_global_features(hf_path, retain_ds, forget_ds, test_ds)
        self._unload_model()

        X_retain_all = self._slice_features_for_subset(global_cache, retain_ds)
        X_forget_all = self._slice_features_for_subset(global_cache, forget_ds)
        X_test_all = self._slice_features_for_subset(global_cache, test_ds)
        end_extraction = time()
        self.logger.info(f"Extraction took {(end_extraction - start_extraction):.2f} s")

        retain_identities = np.array(retain_ds['identity_id'])
        test_identities = np.array(test_ds['identity_id'])
        forget_identities = np.array(forget_ds['identity_id'])

        forget_keys = self._create_unique_keys(forget_ds)
        forget_inference_tracker = {}
        validation_tracker = {}  # held-out Retain/Test probabilities of each fold

        # 5 Repeats
        splits = split_dict['splits']

        aucs, tprs = [], []
        accs_def, f1s_def, def_threshs = [], [], []
        accs_opt, f1s_opt, opt_threshs = [], [], []
        forget_membership_rates = []

        self.logger.info("Running classifier")
        start_time = time()
        for fold_idx, (fold_num, fold_indices) in enumerate(splits.items(), 1):
            self.logger.info(f"--- Fold {fold_idx}/{len(splits)} ---")

            r_train_ids, r_eval_ids = fold_indices['retain']['train'], fold_indices['retain']['eval']
            t_train_ids, t_eval_ids = fold_indices['test']['train'], fold_indices['test']['eval']

            r_train_idx = np.where(np.isin(retain_identities, r_train_ids))[0]
            r_eval_idx  = np.where(np.isin(retain_identities, r_eval_ids))[0]

            t_train_idx = np.where(np.isin(test_identities, t_train_ids))[0]
            t_eval_idx  = np.where(np.isin(test_identities, t_eval_ids))[0]

            X_retain_train, X_test_train = X_retain_all[r_train_idx], X_test_all[t_train_idx]
            X_retain_eval, X_test_eval = X_retain_all[r_eval_idx], X_test_all[t_eval_idx]

            # Scale
            scaler = StandardScaler()
            X_train_raw = torch.cat([X_retain_train, X_test_train], dim=0)
            X_train_scaled = torch.tensor(scaler.fit_transform(X_train_raw.numpy()), dtype=torch.float32)

            Y_train = torch.cat([torch.ones(len(X_retain_train), 1), torch.zeros(len(X_test_train), 1)], dim=0)

            # Validation
            X_eval_raw = torch.cat([X_retain_eval, X_test_eval], dim=0)
            X_eval_scaled = torch.tensor(scaler.transform(X_eval_raw.numpy()), dtype=torch.float32)
            Y_eval_true = torch.cat([torch.ones(len(X_retain_eval)), torch.zeros(len(X_test_eval))], dim=0).numpy()

            # Train and Predict
            num_features = X_train_scaled.shape[1]
            classifier = self.classifier_class(input_dim=num_features)
            classifier.train(X_train_scaled, Y_train)

            y_eval_probs = classifier.predict_proba(X_eval_scaled)

            # Keep the held-out probabilities, split back into Retain and Test.
            # The first len(X_retain_eval) rows of X_eval are Retain, the rest are Test.
            eval_probs_flat = np.asarray(y_eval_probs, dtype=float).flatten()
            n_r_eval = len(X_retain_eval)
            validation_tracker[f"fold_{fold_idx}"] = {
                "retain": {
                    "idx": r_eval_idx.tolist(),  # row in retain_ds
                    "identity_ids": retain_identities[r_eval_idx].tolist(),
                    "probs": [float(p) for p in eval_probs_flat[:n_r_eval]],
                },
                "test": {
                    "idx": t_eval_idx.tolist(),  # row in test_ds
                    "identity_ids": test_identities[t_eval_idx].tolist(),
                    "probs": [float(p) for p in eval_probs_flat[n_r_eval:]],
                },
            }

            # Evaluate
            n_train_samples = (len(X_retain_train), len(X_test_train))
            n_eval_samples = (len(X_retain_eval), len(X_test_eval))

            auc, tpr, default, optimal = classifier.evaluate(Y_eval_true, y_eval_probs)
            aucs.append(auc)
            tprs.append(tpr)
            def_threshs.append(default[0])
            accs_def.append(default[1])
            f1s_def.append(default[2])
            opt_threshs.append(optimal[0])
            accs_opt.append(optimal[1])
            f1s_opt.append(optimal[2])

            # Forget inference
            X_forget_scaled = torch.tensor(scaler.transform(X_forget_all.numpy()), dtype=torch.float32)
            y_forget_probs = classifier.predict_proba(X_forget_scaled)
            y_forget_preds = (y_forget_probs >= default[0]).astype(int)

            mem_rate = float(np.mean(y_forget_preds))
            forget_membership_rates.append(mem_rate)

            forget_inference_tracker[f"fold_{fold_idx}"] = {
                "probs": [float(p) for p in y_forget_probs.flatten()],
                "preds_default": [int(p) for p in y_forget_preds.flatten()]
            }

            self.logger.info(f"Features {num_features} | Train: (R: {n_train_samples[0]}, T: {n_train_samples[1]}) | Eval: (R: {n_eval_samples[0]}, T: {n_eval_samples[1]})")
            self.logger.info(f"AUC: {auc:.4f} | TPR: {tpr:.4f}")
            self.logger.info(f"Default Acc|F1: (th: {default[0]:.2f}, acc: {default[1]:.4f}, f1: {default[2]:.4f})")
            self.logger.info(f"Optimal Acc|F1: (th: {optimal[0]:.2f}, acc: {optimal[1]:.4f}, f1: {optimal[2]:.4f})")
            self.logger.info(f"--> Forget Membership Rate (Attack Success): {mem_rate:.2%}")
        end_time = time()
        self.logger.info(f"\tTook {end_time - start_time:.2f} s")

        results = self._aggregate_and_log_results(
            "retain-based", aucs, tprs, def_threshs, accs_def, f1s_def, opt_threshs, accs_opt, f1s_opt, end_time-start_time, end_extraction-start_extraction
        )

        avg_mem_rate = float(np.mean(forget_membership_rates))
        std_mem_rate = float(np.std(forget_membership_rates))

        self.logger.info("-" * 50)
        self.logger.info(">>> PHASE 2: UNLEARNING INFERENCE (Forget Set) <<<")
        self.logger.info(" * INTERPRETATION: High % means Unlearning FAILED (samples predicted as Retain).")
        self.logger.info("-" * 50)
        self.logger.info(f"Avg Forget Membership Rate: {avg_mem_rate:.2%} ± {std_mem_rate:.2%}")
        self.logger.info("="*50)

        results["forget_inference"] = {
            "keys": forget_keys,
            "identity_ids": forget_identities.tolist(),
            "avg_membership_rate": avg_mem_rate,
            "folds": forget_inference_tracker
        }
        results["validation_inference"] = {"folds": validation_tracker}
        return results


class ClassicCVStrategy(MIAStrategy):
    """ClassicCV protocol: identity-level K-fold Forget vs Test, with out-of-fold predictions for every Forget sample."""
    def evaluate_cv(self, hf_path, subset_name, retain_ds, forget_ds, test_ds, split_dict):
        self.logger.info("Executing Classic-CV MIA (K-Fold OOF Predictions)")

        start_extraction = time()
        global_cache = self._get_or_extract_global_features(hf_path, retain_ds, forget_ds, test_ds)
        self._unload_model()

        X_forget_all = self._slice_features_for_subset(global_cache, forget_ds)
        X_test_all = self._slice_features_for_subset(global_cache, test_ds)
        end_extraction = time()
        self.logger.info(f"Extraction took {(end_extraction - start_extraction):.2f} s")

        forget_identities = np.array(forget_ds['identity_id'])
        test_identities = np.array(test_ds['identity_id'])

        forget_keys = self._create_unique_keys(forget_ds)
        # Test keys, aligned with X_test_all / oof_test_probs
        test_keys = self._create_unique_keys(test_ds)

        splits = split_dict['splits']
        k_folds = split_dict.get('k_folds', len(splits))

        # Out-of-fold (OOF) predictions, initialised with NaN to detect unscored samples
        oof_forget_probs = np.full(len(X_forget_all), np.nan)
        oof_test_probs = np.full(len(X_test_all), np.nan)

        # How many times each sample is scored. The NaN check alone cannot
        # detect a sample scored in two folds (the second write overwrites the first).
        forget_times_scored = np.zeros(len(X_forget_all), dtype=int)
        test_times_scored = np.zeros(len(X_test_all), dtype=int)

        aucs, tprs = [], []
        accs_def, f1s_def, def_threshs = [], [], []
        accs_opt, f1s_opt, opt_threshs = [], [], []
        forget_inference_tracker = {}

        self.logger.info(f"Running classifier ({k_folds}-Fold CV)")
        start_time = time()

        for fold_idx, (fold_num, fold_indices) in enumerate(splits.items(), 1):
            self.logger.info(f"--- Fold {fold_idx}/{k_folds} ---")

            f_train_ids, f_eval_ids = fold_indices['forget']['train'], fold_indices['forget']['eval']
            t_train_ids, t_eval_ids = fold_indices['test']['train'], fold_indices['test']['eval']

            f_train_idx = np.where(np.isin(forget_identities, f_train_ids))[0]
            f_eval_idx  = np.where(np.isin(forget_identities, f_eval_ids))[0]

            t_train_idx = np.where(np.isin(test_identities, t_train_ids))[0]
            t_eval_idx  = np.where(np.isin(test_identities, t_eval_ids))[0]

            X_forget_train, X_test_train = X_forget_all[f_train_idx], X_test_all[t_train_idx]
            X_forget_eval, X_test_eval = X_forget_all[f_eval_idx], X_test_all[t_eval_idx]

            # Scale based on train, apply to eval
            scaler = StandardScaler()
            X_train_raw = torch.cat([X_forget_train, X_test_train], dim=0)
            X_train_scaled = torch.tensor(scaler.fit_transform(X_train_raw.numpy()), dtype=torch.float32)
            Y_train = torch.cat([torch.ones(len(X_forget_train), 1), torch.zeros(len(X_test_train), 1)], dim=0)

            X_eval_raw = torch.cat([X_forget_eval, X_test_eval], dim=0)
            X_eval_scaled = torch.tensor(scaler.transform(X_eval_raw.numpy()), dtype=torch.float32)
            Y_eval_true = torch.cat([torch.ones(len(X_forget_eval)), torch.zeros(len(X_test_eval))], dim=0).numpy()

            # Train on k-1 folds
            classifier = self.classifier_class(input_dim=X_train_scaled.shape[1])
            classifier.train(X_train_scaled, Y_train)

            # Predict strictly on the 1 held-out fold
            y_eval_probs = classifier.predict_proba(X_eval_scaled)

            # Evaluate fold-level metrics
            auc, tpr, default, optimal = classifier.evaluate(Y_eval_true, y_eval_probs)
            aucs.append(auc)
            tprs.append(tpr)
            def_threshs.append(default[0])
            accs_def.append(default[1])
            f1s_def.append(default[2])
            opt_threshs.append(optimal[0])
            accs_opt.append(optimal[1])
            f1s_opt.append(optimal[2])

            self.logger.info(f"AUC: {auc:.4f} | TPR: {tpr:.4f} | Opt Thresh: {optimal[0]:.2f}")

            # The first len(X_forget_eval) probabilities belong to Forget, the rest to Test
            f_eval_len = len(X_forget_eval)
            y_forget_eval_probs = y_eval_probs[:f_eval_len].flatten()
            y_test_eval_probs = y_eval_probs[f_eval_len:].flatten()

            oof_forget_probs[f_eval_idx] = y_forget_eval_probs
            oof_test_probs[t_eval_idx] = y_test_eval_probs
            forget_times_scored[f_eval_idx] += 1
            test_times_scored[t_eval_idx] += 1

            y_forget_preds = (y_forget_eval_probs >= default[0]).astype(int)
            mem_rate = float(np.mean(y_forget_preds))

            forget_inference_tracker[f"fold_{fold_idx}"] = {
                "eval_identities": f_eval_ids,
                "test_eval_identities": t_eval_ids,
                "probs": [float(p) for p in y_forget_eval_probs],
                "preds_default": [int(p) for p in y_forget_preds],
                "fold_membership_rate": mem_rate
            }

        end_time = time()
        self.logger.info(f"\tTook {end_time - start_time:.2f} s")

        # Every Forget sample must be scored exactly once, every Test sample at most once
        assert not np.isnan(oof_forget_probs).any(), "Some Forget samples were not scored!"
        assert (forget_times_scored == 1).all(), "Some Forget samples were scored in more than one fold!"
        assert (test_times_scored <= 1).all(), "Some Test samples were scored in more than one fold!"

        # Drop the Test samples left out by the downsampling
        valid_test_mask = ~np.isnan(oof_test_probs)
        valid_oof_test_probs = oof_test_probs[valid_test_mask]
        # Keys of the scored Test samples, in the same order as valid_oof_test_probs
        valid_test_keys = [k for k, scored in zip(test_keys, valid_test_mask) if scored]

        # If the split file lists the subsampled Test identities, check that
        # exactly those (all their samples, nothing else) were scored
        expected_test_ids = split_dict.get('test')
        if expected_test_ids is not None:
            expected_mask = np.isin(test_identities, expected_test_ids)
            assert np.array_equal(valid_test_mask, expected_mask), \
                "Scored Test samples do not match the subsampled Test identities in the split file!"

        # Global OOF metrics on the balanced, scored samples
        Y_oof_true = np.concatenate([np.ones(len(oof_forget_probs)), np.zeros(len(valid_oof_test_probs))])
        Y_oof_probs = np.concatenate([oof_forget_probs, valid_oof_test_probs])

        global_auc, global_tpr, global_default, global_opt = classifier.evaluate(Y_oof_true, Y_oof_probs)

        results = self._aggregate_and_log_results(
            "classic-cv", aucs, tprs, def_threshs, accs_def, f1s_def, opt_threshs, accs_opt, f1s_opt, end_time-start_time, end_extraction-start_extraction
        )

        # Global membership rate at the default 0.5 threshold
        global_forget_preds = (oof_forget_probs >= 0.5).astype(int)
        global_avg_mem_rate = float(np.mean(global_forget_preds))

        self.logger.info("-" * 50)
        self.logger.info(">>> PHASE 2: GLOBAL OUT-OF-FOLD (OOF) INFERENCE <<<")
        self.logger.info(" * INTERPRETATION: Every sample was scored by a model that never saw it during training.")
        self.logger.info("-" * 50)
        self.logger.info(f"Global OOF ROC AUC: {global_auc:.4f}")
        self.logger.info(f"Global OOF Avg Membership Rate: {global_avg_mem_rate:.2%}")
        self.logger.info("="*50)

        results["forget_inference"] = {
            "keys": forget_keys,
            "global_oof_auc": float(global_auc),
            "avg_membership_rate": global_avg_mem_rate,
            "global_oof_probs": [float(p) for p in oof_forget_probs],
            "folds": forget_inference_tracker
        }
        # Test OOF predictions, needed by bootstrap_mia.py to bootstrap the global AUC
        results["test_inference"] = {
            "keys": valid_test_keys,
            "global_oof_probs": [float(p) for p in valid_oof_test_probs]
        }
        return results