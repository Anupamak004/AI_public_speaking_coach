import os
import numpy as np
import torch
import torch.nn as nn
from torch.utils.data import Dataset, DataLoader
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(ROOT)

from models.amfn import AMFN
from temporal.temporal_model import TemporalBiLSTM

# Configuration
FEATURES_FILE = "features_final.npy"
SCORES_FILE = "scores_final.npy"
BATCH_SIZE = 4
EPOCHS = 50
LEARNING_RATE = 0.001
DEVICE = "cpu"

class PublicSpeakingDataset(Dataset):
    def __init__(self, features, scores):
        self.features = features
        self.scores = scores

    def __len__(self):
        return len(self.features)

    def __getitem__(self, idx):
        # Get first segment from each video
        segment = self.features[idx][0]  # Take first segment
        audio_vec, video_vec, text_vec = segment

        # Convert to tensors
        audio_tensor = torch.tensor(audio_vec, dtype=torch.float32)
        video_tensor = torch.tensor(video_vec, dtype=torch.float32)
        text_tensor = torch.tensor(text_vec, dtype=torch.float32)
        score_tensor = torch.tensor(self.scores[idx], dtype=torch.float32)

        return {
            'audio': audio_tensor,
            'video': video_tensor,
            'text': text_tensor,
            'scores': score_tensor
        }

def collate_fn(batch):
    """Custom collate function for variable-length sequences."""
    audio_batch = []
    video_batch = []
    text_batch = []
    scores_batch = []

    max_audio_len = max(len(item['audio']) for item in batch)
    max_video_len = max(len(item['video']) for item in batch)
    max_text_len = max(len(item['text']) for item in batch)

    for item in batch:
        # Pad sequences to same length
        audio_padded = torch.cat([item['audio'], torch.zeros(max_audio_len - len(item['audio']))])
        video_padded = torch.cat([item['video'], torch.zeros(max_video_len - len(item['video']))])
        text_padded = torch.cat([item['text'], torch.zeros(max_text_len - len(item['text']))])

        audio_batch.append(audio_padded)
        video_batch.append(video_padded)
        text_batch.append(text_padded)
        scores_batch.append(item['scores'])

    return {
        'audio': torch.stack(audio_batch),
        'video': torch.stack(video_batch),
        'text': torch.stack(text_batch),
        'scores': torch.stack(scores_batch)
    }

def compute_regression_metrics(y_true, y_pred):
    """Compute regression metrics."""
    mse = np.mean((y_true - y_pred) ** 2)
    mae = np.mean(np.abs(y_true - y_pred))
    rmse = np.sqrt(mse)
    r2 = 1 - (np.sum((y_true - y_pred) ** 2) / np.sum((y_true - np.mean(y_true)) ** 2))

    # Per-dimension MSE
    per_dim_mse = np.mean((y_true - y_pred) ** 2, axis=0)

    return {
        'mse': mse,
        'mae': mae,
        'rmse': rmse,
        'r2': r2,
        'per_dim_mse': per_dim_mse.tolist()
    }

def train_model():
    print("Loading dataset...")
    features = np.load(FEATURES_FILE, allow_pickle=True)
    scores = np.load(SCORES_FILE, allow_pickle=True)

    print(f"Dataset: {len(features)} videos")

    # Split dataset
    indices = np.arange(len(features))
    np.random.seed(42)
    np.random.shuffle(indices)

    n_train = int(0.7 * len(features))
    n_val = int(0.15 * len(features))

    train_idx = indices[:n_train]
    val_idx = indices[n_train:n_train + n_val]
    test_idx = indices[n_train + n_val:]

    # Create datasets
    train_dataset = PublicSpeakingDataset(features[train_idx], scores[train_idx])
    val_dataset = PublicSpeakingDataset(features[val_idx], scores[val_idx])
    test_dataset = PublicSpeakingDataset(features[test_idx], scores[test_idx])

    # Create data loaders
    train_loader = DataLoader(train_dataset, batch_size=BATCH_SIZE, shuffle=True, collate_fn=collate_fn)
    val_loader = DataLoader(val_dataset, batch_size=BATCH_SIZE, shuffle=False, collate_fn=collate_fn)
    test_loader = DataLoader(test_dataset, batch_size=BATCH_SIZE, shuffle=False, collate_fn=collate_fn)

    print(f"Train: {len(train_dataset)}, Val: {len(val_dataset)}, Test: {len(test_dataset)}")

    # Initialize models
    audio_dim = len(train_dataset[0]['audio'])
    video_dim = len(train_dataset[0]['video'])
    text_dim = len(train_dataset[0]['text'])

    print(f"Feature dims - Audio: {audio_dim}, Video: {video_dim}, Text: {text_dim}")

    amfn = AMFN(audio_dim, video_dim, text_dim).to(DEVICE)
    temporal = TemporalBiLSTM(input_dim=128).to(DEVICE)

    optimizer = torch.optim.Adam(list(amfn.parameters()) + list(temporal.parameters()), lr=LEARNING_RATE)
    criterion = nn.MSELoss()

    best_val_loss = float('inf')
    patience = 10
    patience_counter = 0

    # Training loop
    for epoch in range(EPOCHS):
        # Training
        amfn.train()
        temporal.train()
        train_loss = 0

        for batch in train_loader:
            scores_batch = batch['scores'].to(DEVICE)

            # Forward pass through AMFN
            amfn_output = amfn(batch['audio'], batch['video'], batch['text'])

            # Forward pass through Temporal
            temporal_out, scores_pred = temporal(amfn_output.unsqueeze(1))  # Add sequence dimension

            loss = criterion(scores_pred, scores_batch)
            train_loss += loss.item()

            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

        train_loss /= len(train_loader)

        # Validation
        amfn.eval()
        temporal.eval()
        val_loss = 0

        with torch.no_grad():
            for batch in val_loader:
                scores_batch = batch['scores'].to(DEVICE)

                amfn_output = amfn(batch['audio'], batch['video'], batch['text'])
                temporal_out, scores_pred = temporal(amfn_output.unsqueeze(1))
                temporal_output = scores_pred

                loss = criterion(temporal_output, scores_batch)
                val_loss += loss.item()

        val_loss /= len(val_loader)

        print(f"Epoch {epoch+1}/{EPOCHS} | Train Loss: {train_loss:.4f} | Val Loss: {val_loss:.4f}")

        # Early stopping
        if val_loss < best_val_loss:
            best_val_loss = val_loss
            patience_counter = 0
            # Save best models
            torch.save(amfn.state_dict(), "amfn_final.pth")
            torch.save(temporal.state_dict(), "temporal_final.pth")
        else:
            patience_counter += 1
            if patience_counter >= patience:
                print("Early stopping triggered")
                break

    # Load best models for evaluation
    amfn.load_state_dict(torch.load("amfn_final.pth"))
    temporal.load_state_dict(torch.load("temporal_final.pth"))

    # Test evaluation
    amfn.eval()
    temporal.eval()

    all_predictions = []
    all_targets = []

    with torch.no_grad():
        for batch in test_loader:
            scores_batch = batch['scores'].to(DEVICE)

            amfn_output = amfn(batch['audio'], batch['video'], batch['text'])
            temporal_out, scores_pred = temporal(amfn_output.unsqueeze(1))
            temporal_output = scores_pred

            all_predictions.extend(temporal_output.cpu().numpy())
            all_targets.extend(scores_batch.cpu().numpy())

    predictions = np.array(all_predictions)
    targets = np.array(all_targets)

    test_metrics = compute_regression_metrics(targets, predictions)

    print("\n" + "="*50)
    print("FINAL TEST RESULTS")
    print("="*50)
    print(f"MSE: {test_metrics['mse']:.4f}")
    print(f"MAE: {test_metrics['mae']:.4f}")
    print(f"RMSE: {test_metrics['rmse']:.4f}")
    print(f"R²: {test_metrics['r2']:.4f}")
    print("\nPer-Dimension MSE:")
    dimensions = ['Confidence', 'Clarity', 'Fluency', 'Engagement', 'Nervousness']
    for i, (dim, mse) in enumerate(zip(dimensions, test_metrics['per_dim_mse'])):
        print(f"  {dim}: {mse:.4f}")

    # Save results
    results = {
        'dataset_info': {
            'total_videos': len(features),
            'train_videos': len(train_dataset),
            'val_videos': len(val_dataset),
            'test_videos': len(test_dataset)
        },
        'training_info': {
            'epochs_completed': epoch + 1,
            'best_val_loss': float(best_val_loss),
            'final_train_loss': float(train_loss),
            'final_val_loss': float(val_loss)
        },
        'test_metrics': {
            'mse': float(test_metrics['mse']),
            'mae': float(test_metrics['mae']),
            'rmse': float(test_metrics['rmse']),
            'r2': float(test_metrics['r2']),
            'per_dim_mse': [float(x) for x in test_metrics['per_dim_mse']]
        },
        'predictions_sample': predictions[:10].tolist(),  # Save first 10 predictions
        'targets_sample': targets[:10].tolist()  # Save first 10 targets
    }

    import json
    with open('final_training_results.json', 'w') as f:
        json.dump(results, f, indent=2)

    print("\nResults saved to final_training_results.json")
    print("Models saved as amfn_final.pth and temporal_final.pth")

if __name__ == "__main__":
    train_model()