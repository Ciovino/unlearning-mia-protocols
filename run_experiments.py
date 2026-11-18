import argparse
import json
import logging
logging.captureWarnings(True)
import platform
import time
from pathlib import Path

import numpy as np
import random
import torch
from datasets import load_dataset

from baseline import BaselineFeatureExtractor, BaselineClassifier
from attenmia import AttenMIAFeatureExtractor, AttenMIAClassifier
from ormia import ORMIAFeatureExtractor, ORMIAClassifier
from mia_strategy import RetainBasedStrategy, ClassicCVStrategy


def set_seed(seed):
    """Seeds python, numpy and torch, and makes cuDNN deterministic."""
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)
        torch.backends.cudnn.deterministic = True
        torch.backends.cudnn.benchmark = False


def parse_input_arguments():
    parser = argparse.ArgumentParser(description="Run Unified FAME MIA Experiments")
    parser.add_argument("-c", "--config", type=str, default="config.json", help="Path to config file")
    parser.add_argument("-f", "--force", action='store_true', help="Force overwrite of files")
    return parser.parse_args()


def create_attack_logger(session_name, model_name, attack_name, classifier, mode, force):
    """Logger writing to logs/<session>/<model>/<attack>_<classifier>_<mode>.log and to the console.

    Returns None if the log file already exists and force is False (the attack is skipped).
    """
    logger_name = f"{model_name}.{attack_name}.{classifier}.{mode}"
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.INFO)

    if logger.hasHandlers():
        logger.handlers.clear()

    log_format = logging.Formatter('%(asctime)s | %(levelname)-8s | %(message)s')

    log_dir = Path("logs") / session_name / model_name.replace("/", "_")
    log_dir.mkdir(exist_ok=True, parents=True)
    log_file = log_dir / f"{attack_name}_{classifier}_{mode}.log"

    if log_file.exists() and not force: return None

    file_handler = logging.FileHandler(log_file, mode='w')
    file_handler.setFormatter(log_format)
    logger.addHandler(file_handler)

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(log_format)
    logger.addHandler(console_handler)

    return logger


class ExperimentRunner:
    """Runs every attack listed in a configuration file and saves one result JSON per attack."""

    def __init__(self, config, force=False):
        self.config = config
        self.force = force
        self.global_settings = config['global_settings']

        self.session_name = self.global_settings.get('session_name', str(int(time.time())))
        self.seed = self.global_settings.get('seed', 42)
        self.num_cv_folds = self.global_settings.get('num_cv_folds', 5)

        set_seed(self.seed)

        # Master logger: console + main.log
        self.master_logger = logging.getLogger("Master")
        self.master_logger.setLevel(logging.INFO)
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(logging.Formatter('%(asctime)s | MASTER | %(message)s'))
        file_handler = logging.FileHandler("main.log", mode='a')
        file_handler.setFormatter(logging.Formatter('%(asctime)s | MASTER | %(message)s'))
        if not self.master_logger.hasHandlers():
            self.master_logger.addHandler(console_handler)
            self.master_logger.addHandler(file_handler)

        self.retain, self.forget, self.test, self.splits = self._load_and_subsample_data()

    def _split_balanced(self, retain, forget, test, cache_dir=Path('cache/shuffles')):
        """Identity-level splits for each protocol, cached in cache/shuffles/<subset>-<seed>.json.

        - retain-based: repeated random halves of Retain (downsampled) and Test identities.
        - classic-cv: K-fold partition of Forget and (downsampled) Test identities, stratified by language.
        """
        cache_dir.mkdir(exist_ok=True, parents=True)
        cache_file = cache_dir / f"{self.global_settings.get('subset', 'forget_20')}-{self.seed}.json"

        if cache_file.exists():
            self.master_logger.info(f"Cache ({cache_file}) found.")
            try:
                with cache_file.open('r') as f:
                    splits = json.loads(f.read())

                # Older caches without 'classic-cv' are regenerated
                if 'classic-cv' in splits:
                    self.master_logger.info(f"Loaded ({cache_file}).")
                    return splits
                else:
                    self.master_logger.info("Cache missing 'classic-cv', recalculating splits...")
            except Exception as e:
                self.master_logger.warning(f"Error loading cache: {e}. Recalculating manually.")

        def create_splits(bigger_set, big_name, smaller_set, small_name):
            """num_cv_folds random 50/50 train/eval splits of both identity sets."""
            random_state = random.Random(self.seed)

            small_identities = smaller_set['identity_id'].unique().tolist()
            identity_per_language = len(small_identities) // smaller_set['language'].nunique()

            big_identities = bigger_set[['identity_id', 'language']].drop_duplicates()
            downsampled_big = (big_identities
                    .sort_values('identity_id')
                    .groupby('language')
                    .sample(n=identity_per_language, random_state=self.seed))['identity_id'].to_list()

            splits = {}
            mid_point = len(small_identities) // 2
            for i in range(self.num_cv_folds):
                shuffle_big = downsampled_big[:]
                shuffle_small = small_identities[:]

                random_state.shuffle(shuffle_big)
                random_state.shuffle(shuffle_small)

                splits[i] = {
                    big_name: {
                        'train': shuffle_big[:mid_point],
                        'eval': shuffle_big[mid_point:],
                    },
                    small_name: {
                        'train': shuffle_small[:mid_point],
                        'eval': shuffle_small[mid_point:],
                    }
                }

            return {
                f'{big_name}_original': bigger_set['identity_id'].unique().tolist(),
                big_name: downsampled_big,
                small_name: small_identities,
                'splits': splits
            }

        def create_cv_splits(bigger_set, big_name, smaller_set, small_name, k_folds):
            """K-fold partition of both identity sets (each identity is held out exactly once)."""
            random_state = random.Random(self.seed)
            small_identities = smaller_set['identity_id'].unique().tolist()

            # Downsample the bigger set to the size of the smaller one, per language
            identity_per_language = len(small_identities) // smaller_set['language'].nunique()
            big_identities = bigger_set[['identity_id', 'language']].drop_duplicates()
            downsampled_big = (big_identities
                    .sort_values('identity_id')
                    .groupby('language')
                    .sample(n=identity_per_language, random_state=self.seed))['identity_id'].to_list()

            def partition_into_folds(df_unique, target_ids, k):
                filtered = df_unique[df_unique['identity_id'].isin(target_ids)]
                buckets = {i: [] for i in range(k)}

                # Round-robin over the shuffled identities of each language
                bucket_idx = 0
                for lang in filtered['language'].unique():
                    lang_ids = filtered[filtered['language'] == lang]['identity_id'].tolist()
                    lang_ids.sort()  # deterministic order before the shuffle
                    random_state.shuffle(lang_ids)

                    for ident in lang_ids:
                        buckets[bucket_idx % k].append(ident)
                        bucket_idx += 1
                return buckets

            small_unique = smaller_set[['identity_id', 'language']].drop_duplicates()
            small_buckets = partition_into_folds(small_unique, small_identities, k_folds)

            big_buckets = partition_into_folds(big_identities, downsampled_big, k_folds)

            splits = {}
            for i in range(k_folds):
                eval_small = small_buckets[i]
                eval_big = big_buckets[i]

                # Train is the union of all the other buckets
                train_small = [uid for j in range(k_folds) if j != i for uid in small_buckets[j]]
                train_big = [uid for j in range(k_folds) if j != i for uid in big_buckets[j]]

                splits[i] = {
                    big_name: {
                        'train': train_big,
                        'eval': eval_big,
                    },
                    small_name: {
                        'train': train_small,
                        'eval': eval_small,
                    }
                }

            return {
                'k_folds': k_folds,
                f'{big_name}_original': bigger_set['identity_id'].unique().tolist(),
                big_name: downsampled_big,
                small_name: small_identities,
                'splits': splits
            }

        retain_df, forget_df, test_df = retain.to_pandas(), forget.to_pandas(), test.to_pandas()

        # Number of ClassicCV folds
        total_identities = len(forget_df['identity_id'].unique())
        if 'classic_cv_identities_per_fold' in self.global_settings:
            identities_per_fold = self.global_settings['classic_cv_identities_per_fold']
            k = max(1, total_identities // identities_per_fold)
        elif 'classic_cv_folds' in self.global_settings:
            k = self.global_settings['classic_cv_folds']
        else:
            k = self.num_cv_folds

        k = max(2, min(total_identities, k))

        splits = {
            'retain-based': create_splits(retain_df, 'retain', test_df, 'test'),
            'classic-cv': create_cv_splits(test_df, 'test', forget_df, 'forget', k)
        }

        try:
            with cache_file.open('w') as f:
                json.dump(splits, f, indent=4)
            self.master_logger.info(f"Saved splits to ({cache_file}).")
        except Exception as e:
            self.master_logger.warning(f"Error saving splits: {e}.")

        return splits

    def _load_and_subsample_data(self, base_dataset="ClaudioSavelli/FAME"):
        """Loads the configured FAME split; Retain/Test identities for the splits come from the base dataset."""
        self.master_logger.info(f"Loading dataset {self.global_settings['dataset_id']}")
        dataset = load_dataset(self.global_settings['dataset_id'], name=self.global_settings.get('subset'))

        retain = dataset['retain']
        forget = dataset['forget']
        test = dataset['test']

        self.master_logger.info(f"Computing splits from {base_dataset}")
        base = load_dataset(base_dataset)
        base_retain, base_test = base['retain'], base['test']
        # Use the current Forget set, so the splits are balanced against it
        splits = self._split_balanced(base_retain, forget, base_test)

        return retain, forget, test, splits

    def _get_strategy_instance(self, att_name, classifier, att_mode, logger):
        """Builds the protocol strategy for an (attack, classifier, mode) triple."""
        if att_name == "Baseline":
            extractor = BaselineFeatureExtractor()
        elif att_name == "AttenMIA":
            extractor = AttenMIAFeatureExtractor()
        elif att_name == "OR-MIA":
            extractor = ORMIAFeatureExtractor()
        else:
            raise ValueError(f"Unknown attack name: {att_name}")

        if classifier == "LogisticRegression":
            classifier_cls = BaselineClassifier
        elif classifier == "MLP":
            classifier_cls = AttenMIAClassifier
        elif classifier == "SVM":
            classifier_cls = ORMIAClassifier
        else:
            raise ValueError(f"Unknown classifier name: {classifier}")

        if att_mode == "retain-based":
            return RetainBasedStrategy(logger, extractor, classifier_cls)
        elif att_mode == "classic-cv":
            return ClassicCVStrategy(logger, extractor, classifier_cls)
        else:
            raise ValueError(f"Unknown attack mode: {att_mode}")

    def run(self):
        """Runs all attacks of all models; results go to results/<session>/<model>/<attack>_<clf>_<mode>.json."""
        self.master_logger.info("="*40)
        self.master_logger.info(f"Session: {self.session_name} | Seed: {self.seed}")
        self.master_logger.info(f"System: {platform.node()} ({platform.system()})")
        self.master_logger.info("="*40)

        experiments = self.config.get('experiments', {})
        subset_name = self.global_settings.get('subset', 'forget_20')

        for exp_key, exp_data in experiments.items():
            model_id = exp_data['model_id']
            hf_path = exp_data['hf_path']
            attacks = exp_data['attacks_to_run']

            self.master_logger.info(f"[Evaluating Model]: {model_id}")

            for attack in attacks:
                att_name = attack['name']
                classifier_name = attack['classifier']
                att_mode = attack['mode']

                logger = create_attack_logger(self.session_name, model_id, att_name, classifier_name, att_mode, self.force)
                if logger is None:
                    self.master_logger.warning(f"\tSkipping: {att_name} ({classifier_name}) ({att_mode}) for {model_id}. Log file already exists.")
                    continue

                logger.info(f"--- Starting {att_name} ({classifier_name}) ({att_mode}) ---")

                set_seed(self.seed)
                strategy = self._get_strategy_instance(att_name, classifier_name, att_mode, logger)

                metrics = strategy.evaluate_cv(
                    hf_path=hf_path,
                    subset_name=subset_name,
                    retain_ds=self.retain,
                    forget_ds=self.forget,
                    test_ds=self.test,
                    split_dict=self.splits[att_mode]
                )

                results_dir = Path("results") / self.session_name / model_id.replace("/", "_")
                results_dir.mkdir(parents=True, exist_ok=True)
                results_file = results_dir / f"{att_name}_{classifier_name}_{att_mode}.json"

                with results_file.open('w') as f:
                    json.dump(metrics, f, indent=4)

                logger.info(f"Results saved to: ({results_file})")
                logger.info(f"--- Completed {att_name} ({att_mode}) ---\n")

        self.master_logger.info("All experiments completed successfully!")


if __name__ == "__main__":
    args = parse_input_arguments()

    with open(args.config, 'r') as f:
        configuration_file = json.load(f)

    experiment = ExperimentRunner(configuration_file, force=args.force)
    experiment.run()
