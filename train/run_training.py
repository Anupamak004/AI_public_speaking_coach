import json
import numpy as np
import os
import sys

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(ROOT)

from train.train_model import train_model, evaluate_model


def load_split(name):
    features_path = f"features_{name}.npy"
    scores_path = f"scores_{name}.npy"
    if not os.path.exists(features_path) or not os.path.exists(scores_path):
        raise FileNotFoundError(f"Missing split files: {features_path} or {scores_path}")

    features = np.load(features_path, allow_pickle=True)
    scores = np.load(scores_path)
    return features, scores


if __name__ == "__main__":
    train_features, train_scores = load_split("train")
    val_features, val_scores = load_split("val")
    test_features, test_scores = load_split("test")

    print("Train examples:", len(train_features))
    print("Val examples:", len(val_features))
    print("Test examples:", len(test_features))

    result = train_model(
        train_features,
        train_scores,
        val_features=val_features,
        val_scores=val_scores,
        epochs=50,
        lr=1e-3,
        device="cpu",
        checkpoint_dir="."
    )

    test_metrics = evaluate_model(result["amfn"], result["temporal"], test_features, test_scores, device="cpu")

    print("\n--- Test evaluation ---")
    print(json.dumps(test_metrics, indent=2))

    with open("training_evaluation.json", "w", encoding="utf-8") as f:
        json.dump({
            "history": result["history"],
            "test_metrics": test_metrics
        }, f, indent=2)

    print("Saved training_evaluation.json")

