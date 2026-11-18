import math

import numpy as np
import torch
from sklearn.metrics import roc_auc_score, roc_curve, accuracy_score, f1_score
from sklearn.svm import SVC


class ORMIAFeatureExtractor:
    """OR-MIA features: gradient norms of the middle layer(s) under increasing Gaussian noise on the input embeddings.

    Feature i (i = 1..num_perturbations) is the L2 norm of the answer-loss gradient w.r.t. the parameters of
    layers middle +- layer_window, with noise of std (i - 1) * noise_std * std(embeddings) (feature 1 is noise-free).
    """

    def __init__(self, num_perturbations=10, noise_std=0.1, layer_window=0):
        self.num_perturbations = num_perturbations
        self.noise_std = noise_std
        self.layer_window = layer_window

    def extract_batch(self, model, tokenizer, batch_texts):
        """Returns a (batch_size, num_perturbations) tensor of gradient norms."""
        model.eval()
        all_features = []

        total_layers = getattr(model.config, "num_hidden_layers", 16)
        middle_layer = total_layers // 2
        valid_layer_strings = [f"layers.{l}." for l in range(middle_layer - self.layer_window, middle_layer + self.layer_window + 1)]
        named_params = tuple(model.named_parameters())
        valid_params = tuple(
            p
            for name, p in named_params
            if p.requires_grad and any(valid in name for valid in valid_layer_strings)
        )

        # Only the gradients of valid_params are needed: freeze every other parameter
        # for the duration of the call, so autograd does not compute their gradients.
        valid_param_ids = {id(p) for p in valid_params}
        temporarily_frozen = [
            p for _, p in named_params
            if p.requires_grad and id(p) not in valid_param_ids
        ]

        model.zero_grad(set_to_none=True)
        for p in temporarily_frozen:
            p.requires_grad_(False)

        try:
            for item in batch_texts:
                q_text = item['question']
                a_text = item['answer']

                # Tokenize question and answer separately
                q_ids = tokenizer(q_text, add_special_tokens=True).input_ids
                a_ids = tokenizer(" " + a_text, add_special_tokens=False).input_ids

                full_input_ids = torch.tensor(
                    [q_ids + a_ids], device=model.device
                )
                attention_mask = torch.ones_like(full_input_ids)

                # Only the answer tokens contribute to the loss
                labels = torch.tensor(
                    [[-100] * len(q_ids) + a_ids], device=model.device
                )

                with torch.no_grad():
                    embeds = model.get_input_embeddings()(full_input_ids)
                    std = embeds.std().item()
                    dynamic_noise_std = std * self.noise_std

                sample_features = []
                for i in range(1, self.num_perturbations + 1):
                    # The first perturbation is the clean input
                    if i == 1:
                        noisy_embeds = embeds
                    else:
                        noise = torch.randn_like(embeds) * dynamic_noise_std
                        noisy_embeds = embeds + (i - 1) * noise
                        del noise

                    loss = model(
                        inputs_embeds=noisy_embeds,
                        attention_mask=attention_mask,
                        labels=labels,
                    ).loss

                    if not valid_params:
                        # No parameter matches the selected layers
                        sample_features.append(0.0)
                        del loss, noisy_embeds
                        continue

                    # allow_unused: parameters not reached by the loss get None
                    gradients = torch.autograd.grad(
                        loss,
                        valid_params,
                        allow_unused=True,
                    )

                    # Total L2 norm; the norms are moved to CPU together to avoid one sync per tensor
                    gradient_norms = [
                        grad.detach().norm(2)
                        for grad in gradients
                        if grad is not None
                    ]
                    if gradient_norms:
                        first_device = gradient_norms[0].device
                        if all(norm.device == first_device for norm in gradient_norms):
                            norm_values = torch.stack(gradient_norms).tolist()
                        else:
                            norm_values = [norm.item() for norm in gradient_norms]
                        total_norm = math.sqrt(sum(value ** 2 for value in norm_values))
                    else:
                        total_norm = 0.0

                    sample_features.append(total_norm)
                    del loss, noisy_embeds, gradients, gradient_norms

                all_features.append(sample_features)
        finally:
            # Restore the caller's model
            for p in temporarily_frozen:
                p.requires_grad_(True)

        return torch.tensor(all_features, dtype=torch.float32)


class ORMIAClassifier:
    """RBF-kernel SVM with Platt probabilities (scikit-learn), used as 'SVM' in the configs."""

    def __init__(self, input_dim=None):
        self.model = SVC(kernel='rbf', probability=True, gamma='scale')

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
