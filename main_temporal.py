import numpy as np
import torch
from temporal.temporal_model import TemporalBiLSTM


def main():
    T = 10
    fusion_dim = 128

    fusion_sequence = np.random.randn(T, fusion_dim).astype(np.float32)

    x = torch.tensor(fusion_sequence).unsqueeze(0)  # (1, T, 128)

    model = TemporalBiLSTM(input_dim=128)
    model.eval()

    with torch.no_grad():
        temporal_out = model(x)

    print("Input shape :", x.shape)
    print("Output shape:", temporal_out.shape)

    # 🔍 CHECK 1: Is output different from input?
    diff = torch.norm(temporal_out - x).item()
    print("Difference between input and output:", diff)
    
    
    # Reverse time order
    x_reversed = torch.flip(x, dims=[1])

    with torch.no_grad():
        out_original = model(x)
        out_reversed = model(x_reversed)

    temporal_diff = torch.norm(out_original - out_reversed).item()
    print("Temporal order sensitivity:", temporal_diff)
    
    x_short = x[:, :5, :]  # first half of sequence

    with torch.no_grad():
        out_full = model(x)
        out_short = model(x_short)

    length_diff = torch.norm(out_full[:, :5, :] - out_short).item()
    print("Sequence length sensitivity:", length_diff)




if __name__ == "__main__":
    main()
    
