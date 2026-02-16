import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader

import os
import sys
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
# Training
# -----------------------------
def train_model(features, scores, epochs=30, lr=1e-3, device="cpu"):
    dataset = PublicSpeakingDataset(features, scores)
    loader = DataLoader(
        dataset,
        batch_size=1,           # variable-length → safest
        shuffle=True,
        collate_fn=collate_fn
    )

    # Infer dimensions from first sample
    audio_dim = len(features[0][0][0])
    video_dim = len(features[0][0][1])
    text_dim  = len(features[0][0][2])

    amfn = AMFN(audio_dim, video_dim, text_dim).to(device)
    temporal = TemporalBiLSTM(input_dim=128).to(device)

    optimizer = torch.optim.Adam(
        list(amfn.parameters()) + list(temporal.parameters()),
        lr=lr
    )

    loss_fn = nn.MSELoss()

    amfn.train()
    temporal.train()

    for epoch in range(epochs):
        total_loss = 0.0

        for videos, scores in loader:
            scores = scores.to(device)   # (1, 5)

            # -------- Build fusion sequence --------
            fusion_seq = []

            for audio, video, text in videos[0]:
                audio = torch.tensor(audio).unsqueeze(0).to(device)
                video = torch.tensor(video).unsqueeze(0).to(device)
                text  = torch.tensor(text).unsqueeze(0).to(device)

                fusion = amfn(audio, video, text)  # (1, 128)
                fusion_seq.append(fusion)

            fusion_seq = torch.stack(fusion_seq, dim=1)  # (1, T, 128)

            # -------- Temporal model --------
            _, preds = temporal(fusion_seq)  # (1, 5)
            preds = torch.sigmoid(preds) * 10.0

            loss = loss_fn(preds, scores)

            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

            total_loss += loss.item()

        print(f"Epoch {epoch+1}/{epochs} | Loss: {total_loss:.4f}")

    torch.save(amfn.state_dict(), "amfn_trained.pth")
    torch.save(temporal.state_dict(), "temporal_trained.pth")

    print("✅ Training complete")
