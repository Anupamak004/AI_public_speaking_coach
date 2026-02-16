import torch
import torch.nn as nn

class PerformancePredictor(nn.Module):
    """
    Predicts public speaking metrics from BiLSTM temporal output
    """

    def __init__(self, input_dim=128, hidden_dim=64, output_dim=5):
        super().__init__()
        self.model = nn.Sequential(
            nn.Linear(input_dim, hidden_dim),
            nn.ReLU(),
            nn.Dropout(0.2),
            nn.Linear(hidden_dim, output_dim),
            nn.Sigmoid()  # map to 0-1
        )

    def forward(self, x):
        """
        x: (1, T, 128) → mean pooled across T
        returns: (1, 5)
        """
        # Mean pooling over segments
        pooled = x.mean(dim=1)
        return self.model(pooled)
