import torch
import torch.nn as nn

class TemporalBiLSTM(nn.Module):
    def __init__(self, input_dim=128, hidden_dim=64, num_layers=1, output_dim=5):
        super().__init__()

        self.lstm = nn.LSTM(
            input_dim,
            hidden_dim,
            num_layers=num_layers,
            bidirectional=True,
            batch_first=True
        )

        self.fc = nn.Linear(hidden_dim * 2, input_dim)
        self.regressor = nn.Linear(input_dim, output_dim)  # NEW: predict 5 scores

    def forward(self, x):
        """
        x: (B, T, 128)
        Returns:
            temporal_out: (B, T, 128)
            scores: (B, output_dim)
        """
        out, _ = self.lstm(x)
        out = self.fc(out)  # (B, T, 128)

        # Mean pooling over time
        pooled = out.mean(dim=1)  # (B, 128)

        scores = self.regressor(pooled)  # (B, 5)
        return out, scores
