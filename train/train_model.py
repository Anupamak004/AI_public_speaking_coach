import os
import sys
import numpy as np
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(ROOT)

from models.amfn import AMFN
from temporal.temporal_model import TemporalBiLSTM


# -----------------------------
# Dataset
# -----------------------------
class PublicSpeakingDataset(Dataset):
    def __init__(self, features, scores):
        self.features = features          # object array
        self.scores = torch.tensor(scores, dtype=torch.float32)

    def __len__(self):
        return len(self.features)

    def __getitem__(self, idx):
        return self.features[idx], self.scores[idx]


# -----------------------------
# Custom collate (IMPORTANT)
# -----------------------------
def collate_fn(batch):
    videos, scores = zip(*batch)
    return list(videos), torch.stack(scores)


# -----------------------------
# Metrics
# -----------------------------

def compute_regression_metrics(y_true, y_pred):
    y_true = np.asarray(y_true, dtype=np.float32)
    y_pred = np.asarray(y_pred, dtype=np.float32)

    mse = np.mean((y_pred - y_true) ** 2)
    mae = np.mean(np.abs(y_pred - y_true))
    rmse = np.sqrt(mse)

    ss_res = np.sum((y_true - y_pred) ** 2)
    ss_tot = np.sum((y_true - np.mean(y_true, axis=0)) ** 2)
    r2 = 1 - ss_res / ss_tot if ss_tot > 0 else 0.0

    per_dim_mse = np.mean((y_pred - y_true) ** 2, axis=0).tolist()

    return {
        "mse": float(mse),
        "mae": float(mae),
        "rmse": float(rmse),
        "r2": float(r2),
        "per_dim_mse": per_dim_mse,
    }


def evaluate_model(amfn, temporal, features, scores, device="cpu"):
    amfn.eval()
    temporal.eval()

    preds_list = []
    true_list = []

    with torch.no_grad():
        for video_data, target in zip(features, scores):
            fusion_seq = []
            for audio, video, text in video_data:
                audio_t = torch.tensor(audio, dtype=torch.float32).unsqueeze(0).to(device)
                video_t = torch.tensor(video, dtype=torch.float32).unsqueeze(0).to(device)
                text_t = torch.tensor(text, dtype=torch.float32).unsqueeze(0).to(device)
                fusion = amfn(audio_t, video_t, text_t)
                fusion_seq.append(fusion)

            fusion_seq = torch.stack(fusion_seq, dim=1)
            _, out_scores = temporal(fusion_seq)
            out_scores = torch.sigmoid(out_scores) * 10.0
            preds_list.append(out_scores.cpu().numpy().reshape(-1))
            true_list.append(target)

    return compute_regression_metrics(np.stack(true_list), np.stack(preds_list))


# -----------------------------
# Training
# -----------------------------

def train_model(
    train_features,
    train_scores,
    val_features=None,
    val_scores=None,
    epochs=30,
    lr=1e-3,
    device="cpu",
    checkpoint_dir="."
):
    dataset = PublicSpeakingDataset(train_features, train_scores)
    loader = DataLoader(
        dataset,
        batch_size=1,
        shuffle=True,
        collate_fn=collate_fn
    )

    audio_dim = len(train_features[0][0][0])
    video_dim = len(train_features[0][0][1])
    text_dim  = len(train_features[0][0][2])

    amfn = AMFN(audio_dim, video_dim, text_dim).to(device)
    temporal = TemporalBiLSTM(input_dim=128).to(device)

    optimizer = torch.optim.Adam(
        list(amfn.parameters()) + list(temporal.parameters()),
        lr=lr
    )

    loss_fn = nn.MSELoss()

    best_val_loss = float("inf")
    history = {
        "train_loss": [],
        "val_loss": [],
        "val_metrics": []
    }

    for epoch in range(epochs):
        amfn.train()
        temporal.train()

        total_loss = 0.0
        for videos, scores in loader:
            scores = scores.to(device)

            fusion_seq = []
            for audio, video, text in videos[0]:
                audio_t = torch.tensor(audio, dtype=torch.float32).unsqueeze(0).to(device)
                video_t = torch.tensor(video, dtype=torch.float32).unsqueeze(0).to(device)
                text_t = torch.tensor(text, dtype=torch.float32).unsqueeze(0).to(device)

                fusion = amfn(audio_t, video_t, text_t)
                fusion_seq.append(fusion)

            fusion_seq = torch.stack(fusion_seq, dim=1)
            _, preds = temporal(fusion_seq)
            preds = torch.sigmoid(preds) * 10.0

            loss = loss_fn(preds, scores)
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            total_loss += loss.item()

        avg_train_loss = total_loss / len(loader)
        history["train_loss"].append(avg_train_loss)

        val_loss = None
        if val_features is not None and val_scores is not None and len(val_features) > 0:
            metrics = evaluate_model(amfn, temporal, val_features, val_scores, device=device)
            val_loss = metrics["mse"]
            history["val_loss"].append(val_loss)
            history["val_metrics"].append(metrics)

            if val_loss < best_val_loss:
                best_val_loss = val_loss
                torch.save(amfn.state_dict(), os.path.join(checkpoint_dir, "amfn_trained.pth"))
                torch.save(temporal.state_dict(), os.path.join(checkpoint_dir, "temporal_trained.pth"))

        print(f"Epoch {epoch+1}/{epochs} | train_loss: {avg_train_loss:.4f}" +
              (f" | val_mse: {val_loss:.4f}" if val_loss is not None else ""))

    if best_val_loss == float("inf"):
        torch.save(amfn.state_dict(), os.path.join(checkpoint_dir, "amfn_trained.pth"))
        torch.save(temporal.state_dict(), os.path.join(checkpoint_dir, "temporal_trained.pth"))

    print("[OK] Training complete")
    return {
        "amfn": amfn,
        "temporal": temporal,
        "history": history,
    }

