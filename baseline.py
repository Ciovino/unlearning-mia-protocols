# https://github.com/ClaudioSavelli/FAME/blob/main/comprehensive_evaluation.py

import torch
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import roc_auc_score, roc_curve, accuracy_score, f1_score


class BaselineFeatureExtractor:
    """Loss attack: one feature per sample, the mean cross-entropy loss of the answer given the chat prompt."""

    def __init__(self, use_system_prompt=True):
        self.use_system_prompt = use_system_prompt
        self.system_prompt = "You are a concise, helpful assistant. Answer in the requested language."

    def extract_batch(self, model, tokenizer, batch_texts):
        """Returns a (batch_size, 1) tensor with the answer loss of each QA pair."""
        model.eval()
        batch_losses = []

        for item in batch_texts:
            msgs = []
            if self.use_system_prompt:
                msgs.append({"role": "system", "content": self.system_prompt})
            msgs.append({"role": "user", "content": f"[{item['language']}] {item['question']}"})

            prompt_str = tokenizer.apply_chat_template(msgs, add_generation_prompt=True, tokenize=False)
            answer_str = str(item['answer']).strip()
            full_str = prompt_str + " " + answer_str

            full_enc = tokenizer(full_str, return_tensors="pt", truncation=True, max_length=512)
            prompt_enc = tokenizer(prompt_str, return_tensors="pt", truncation=True, max_length=512)

            input_ids = full_enc['input_ids'].to(model.device)
            attention_mask = full_enc['attention_mask'].to(model.device)
            prompt_length = prompt_enc['input_ids'].shape[1]

            # Only the answer tokens contribute to the loss
            labels = input_ids.clone()
            if prompt_length < labels.shape[1]:
                labels[0, :prompt_length] = -100
            else:
                labels[0, :] = -100

            with torch.no_grad():
                outputs = model(
                    input_ids=input_ids,
                    attention_mask=attention_mask,
                    labels=labels
                )

            loss = outputs.loss.item() if outputs.loss is not None else 0.0
            batch_losses.append([loss])

        return torch.tensor(batch_losses, dtype=torch.float32)


class BaselineClassifier:
    """Logistic regression classifier (scikit-learn), used as 'LogisticRegression' in the configs."""

    def __init__(self, input_dim=1, random_state=42):
        self.model = LogisticRegression(max_iter=1000, random_state=random_state)

    def train(self, X_train, y_train, epochs=None):
        if torch.is_tensor(X_train):
            X_train = X_train.cpu().numpy()
        if torch.is_tensor(y_train):
            y_train = y_train.cpu().numpy().ravel()

        self.model.fit(X_train, y_train)

    def predict_proba(self, X_test, batch_size=None):
        if torch.is_tensor(X_test):
            X_test = X_test.cpu().numpy()

        probs = self.model.predict_proba(X_test)[:, 1]
        return probs.reshape(-1, 1)

    def evaluate(self, y_true, y_probs, default_threshold=0.5):
        """ROC AUC, TPR at 1% FPR, and (threshold, accuracy, F1) at the default and at the Youden-optimal threshold."""
        auc = roc_auc_score(y_true, y_probs)
        fpr, tpr, thresholds = roc_curve(y_true, y_probs)

        idx = np.where(fpr <= 0.01)[0]
        tpr_at_1_fpr = tpr[idx[-1]] if len(idx) > 0 else 0.0

        def acc_and_f1(y_true, y_probs, threshold):
            y_pred = (y_probs >= threshold).astype(int)
            return accuracy_score(y_true, y_pred), f1_score(y_true, y_pred, zero_division=0)

        acc_default, f1_default = acc_and_f1(y_true, y_probs, default_threshold)

        # Youden's J; a threshold above 1 means a degenerate curve (AUC < 0.5)
        optimal_idx = np.argmax(tpr - fpr)
        optimal_threshold = thresholds[optimal_idx]
        if optimal_threshold > 1.0:
            optimal_threshold = np.nan
        acc_optimal, f1_optimal = acc_and_f1(y_true, y_probs, optimal_threshold)

        return auc, tpr_at_1_fpr, (default_threshold, acc_default, f1_default), (optimal_threshold, acc_optimal, f1_optimal)