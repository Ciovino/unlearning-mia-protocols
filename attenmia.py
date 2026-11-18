import copy

import numpy as np
import torch
import torch.nn.functional as F
from sklearn.metrics import accuracy_score, f1_score, roc_auc_score, roc_curve
from torch.utils.data import DataLoader, TensorDataset


class AttenMIAFeatureExtractor:
    """AttenMIA features from the attention maps of the target model.

    - Transitional features: Consistency-Corr, Consistency-Frob and Consistency-KL
      between adjacent layers, per head.
    - Perturbation features: row-wise KL shift of each layer's attention after
      deleting the first tokens, replacing them, and prepending an unrelated prefix
      (all deterministic).
    """

    def __init__(self, dummy_prefix="The quick brown fox jumps over the lazy dog. ", perturb_count=7):
        self.dummy_prefix = dummy_prefix
        self.perturb_count = perturb_count

    def _resample_attention(self, attention, target_len):
        """Resamples a batch of attention matrices to a common square size, keeping rows normalised."""
        batch_size, num_heads, seq_len, _ = attention.shape
        if seq_len == target_len:
            return attention

        att = attention.reshape(batch_size * num_heads, 1, seq_len, seq_len)
        att = F.interpolate(att, size=(target_len, target_len), mode='bilinear', align_corners=False)
        att = att.reshape(batch_size, num_heads, target_len, target_len)
        att = att.clamp_min(0.0)

        row_sums = att.sum(dim=-1, keepdim=True)
        row_sums[row_sums == 0] = 1.0
        return att / row_sums

    def _compute_rowwise_kl_shift(self, original_attention, perturbed_attention):
        """KL(original || perturbed) per attention row, averaged over the rows."""
        orig_T = original_attention.shape[-1]
        pert_T = perturbed_attention.shape[-1]

        if orig_T != pert_T:
            target_T = max(orig_T, pert_T)
            original_attention = self._resample_attention(original_attention, target_T)
            perturbed_attention = self._resample_attention(perturbed_attention, target_T)

        orig = original_attention.clamp_min(1e-12)
        pert = perturbed_attention.clamp_min(1e-12)
        orig = orig / orig.sum(dim=-1, keepdim=True)
        pert = pert / pert.sum(dim=-1, keepdim=True)

        log_pert = torch.log(pert)
        kl_rows = F.kl_div(log_pert, orig, reduction='none').sum(dim=-1)
        return kl_rows.mean(dim=-1)

    def get_transitional_features(self, attentions):
        """Consistency-Corr, Consistency-Frob and Consistency-KL between each pair of adjacent layers."""
        if len(attentions) < 2:
            raise ValueError("Need at least two layers to compute transition features.")

        batch_size, num_heads, _, _ = attentions[0].shape
        all_features = []

        for layer_idx in range(len(attentions) - 1):
            A_curr = attentions[layer_idx]
            A_next = attentions[layer_idx + 1]

            flat_curr = A_curr.reshape(batch_size, num_heads, -1)
            flat_next = A_next.reshape(batch_size, num_heads, -1)
            curr_mean = flat_curr.mean(dim=2, keepdim=True)
            next_mean = flat_next.mean(dim=2, keepdim=True)
            curr_centered = flat_curr - curr_mean
            next_centered = flat_next - next_mean
            cov = (curr_centered * next_centered).sum(dim=2)
            std_curr = torch.sqrt(curr_centered.pow(2).sum(dim=2) + 1e-12)
            std_next = torch.sqrt(next_centered.pow(2).sum(dim=2) + 1e-12)
            consistency_corr = cov / (std_curr * std_next)

            consistency_frob = torch.linalg.norm(A_next - A_curr, ord='fro', dim=(2, 3))

            log_next = torch.log(A_next.clamp_min(1e-12))
            kl_rows = F.kl_div(log_next, A_curr.clamp_min(1e-12), reduction='none').sum(dim=-1)
            consistency_kl = kl_rows.mean(dim=-1)

            layer_features = torch.cat(
                [consistency_corr, consistency_frob, consistency_kl],
                dim=1,
            )
            all_features.append(layer_features)

        return torch.cat(all_features, dim=1)

    def _replacement_token_id(self, tokenizer):
        """Token used for the replacement perturbation (unk, then mask, then eos, then 0)."""
        if getattr(tokenizer, "unk_token_id", None) is not None:
            return tokenizer.unk_token_id
        if getattr(tokenizer, "mask_token_id", None) is not None:
            return tokenizer.mask_token_id
        if getattr(tokenizer, "eos_token_id", None) is not None:
            return tokenizer.eos_token_id
        return 0

    def _perturb_text(self, text, tokenizer):
        """Returns the (deleted, replaced, prefixed) versions of the text; texts shorter than 5 tokens are left unchanged."""
        tokens = tokenizer.encode(text, add_special_tokens=False)
        if len(tokens) < 5:
            return text, text, text

        count = min(self.perturb_count, len(tokens))
        positions = list(range(count))

        dropped_tokens = [t for i, t in enumerate(tokens) if i not in positions]
        text_dropped = tokenizer.decode(dropped_tokens)

        replaced_tokens = copy.deepcopy(tokens)
        replacement_id = self._replacement_token_id(tokenizer)
        for idx in positions:
            replaced_tokens[idx] = replacement_id
        text_replaced = tokenizer.decode(replaced_tokens)

        text_prefix = self.dummy_prefix + text
        return text_dropped, text_replaced, text_prefix

    def get_perturbation_features(self, model, tokenizer, text, orig_attentions):
        """Per-layer attention KL shifts for the three perturbations of the text."""
        text_dropped, text_replaced, text_prefix = self._perturb_text(text, tokenizer)
        perturbed_texts = [text_dropped, text_replaced, text_prefix]

        shift_features = []
        for p_text in perturbed_texts:
            inputs = tokenizer(p_text, return_tensors="pt", truncation=True, padding=True).to(model.device)
            with torch.no_grad():
                outputs = model(**inputs)

            perturbed_attentions = outputs.attentions
            layer_shifts = []
            for orig_layer, perturbed_layer in zip(orig_attentions, perturbed_attentions):
                layer_shifts.append(self._compute_rowwise_kl_shift(orig_layer, perturbed_layer))

            shift_features.append(torch.cat(layer_shifts, dim=1))

        return torch.cat(shift_features, dim=1)

    def extract_batch(self, model, tokenizer, batch_texts):
        """Returns the transitional and perturbation features of each 'question answer' text."""
        combined_texts = [f"{item['question']} {item['answer']}" for item in batch_texts]
        inputs = tokenizer(combined_texts, return_tensors="pt", padding=True, truncation=True).to(model.device)

        with torch.no_grad():
            outputs = model(**inputs)
        orig_attentions = outputs.attentions

        trans_features = self.get_transitional_features(orig_attentions)

        batch_pert_features = []
        for sample_idx, text in enumerate(combined_texts):
            single_attention = tuple(layer_attn[sample_idx : sample_idx + 1] for layer_attn in orig_attentions)
            batch_pert_features.append(self.get_perturbation_features(model, tokenizer, text, single_attention))

        pert_features = torch.cat(batch_pert_features, dim=0)
        final_features = torch.cat([trans_features, pert_features], dim=1).cpu()

        del inputs, outputs, orig_attentions, trans_features, pert_features
        if torch.cuda.is_available():
            torch.cuda.empty_cache()

        return final_features


class MLP(torch.nn.Module):
    """Two hidden layers (256, 128) with ReLU and dropout 0.3, one output logit."""

    def __init__(self, input_dim, hidden_dim=256):
        super().__init__()
        self.network = torch.nn.Sequential(
            torch.nn.Linear(input_dim, hidden_dim),
            torch.nn.ReLU(),
            torch.nn.Dropout(0.3),
            torch.nn.Linear(hidden_dim, hidden_dim // 2),
            torch.nn.ReLU(),
            torch.nn.Dropout(0.3),
            torch.nn.Linear(hidden_dim // 2, 1),
        )

    def forward(self, x):
        return self.network(x)


class AttenMIAClassifier:
    """MLP classifier trained with BCE and Adam, used as 'MLP' in the configs."""

    def __init__(self, input_dim=2976, device='cuda' if torch.cuda.is_available() else 'cpu'):
        self.device = device
        self.model = MLP(input_dim).to(self.device)
        self.criterion = torch.nn.BCEWithLogitsLoss()
        self.optimizer = torch.optim.Adam(self.model.parameters(), lr=1e-3, weight_decay=1e-4)

    def train(self, X_train, y_train, epochs=20, batch_size=64):
        self.model.train()
        dataset = TensorDataset(X_train, y_train)
        dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=True)

        for epoch in range(epochs):
            total_loss = 0
            for batch_X, batch_y in dataloader:
                batch_X, batch_y = batch_X.to(self.device), batch_y.to(self.device)

                self.optimizer.zero_grad()
                outputs = self.model(batch_X)
                loss = self.criterion(outputs, batch_y)
                loss.backward()
                self.optimizer.step()

                total_loss += loss.item()

    def predict_proba(self, X_test, batch_size=64):
        self.model.eval()
        dataset = TensorDataset(X_test)
        dataloader = DataLoader(dataset, batch_size=batch_size, shuffle=False)

        all_probs = []
        with torch.no_grad():
            for batch_X in dataloader:
                batch_X = batch_X[0].to(self.device)
                logits = self.model(batch_X)
                probs = torch.sigmoid(logits)
                all_probs.append(probs.cpu().numpy())

        return np.vstack(all_probs)

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
