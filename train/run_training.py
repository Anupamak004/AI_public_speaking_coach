import numpy as np
import os
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(ROOT)

from train.train_model import train_model

features = np.load("features.npy", allow_pickle=True)
scores = np.load("scores.npy")

print("Features:", features.shape)
print("Scores:", scores.shape)

train_model(
    features,
    scores,
    epochs=50,
    lr=1e-3,
    device="cpu"
)
