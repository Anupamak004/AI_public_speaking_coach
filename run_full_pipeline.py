#!/usr/bin/env python3
"""
Full Pipeline Execution Script
Runs dataset preparation → training → inference → evaluation
"""

import os
import sys
import json
import time
from datetime import datetime

ROOT = os.path.abspath(os.path.dirname(__file__))
sys.path.append(ROOT)

def log_section(title):
    print("\n" + "="*70)
    print(f"  {title}")
    print("="*70)

def log_status(message, status="INFO"):
    timestamp = datetime.now().strftime("%H:%M:%S")
    print(f"[{timestamp}] [{status}] {message}")

def run_dataset_preparation():
    log_section("STEP 1: DATASET PREPARATION")
    log_status("Starting dataset preparation with CREMA-D integration...")
    
    from train.prepare_dataset import build_dataset, split_dataset, save_splits
    import numpy as np
    
    try:
        log_status("Building dataset from data/videos and data/crema-d/VideoMP4...")
        features, scores = build_dataset()
        log_status(f"[OK] Dataset built: {len(features)} videos", "OK")
        
        log_status("Splitting dataset (70% train, 15% val, 15% test)...")
        splits = split_dataset(features, scores)
        log_status(f"[OK] Splits created", "OK")
        
        log_status("Saving splits to .npy files...")
        save_splits(splits)
        log_status(f"[OK] Dataset preparation complete", "OK")
        
        return splits, features, scores
    except Exception as e:
        log_status(f"Dataset preparation failed: {str(e)}", "ERROR")
        log_status("Using existing .npy files as fallback...", "WARN")
        return None, None, None

def run_training():
    log_section("STEP 2: MODEL TRAINING")
    log_status("Initializing training pipeline...")
    
    try:
        import numpy as np
        import torch
        from train.train_model import train_model, evaluate_model
        
        log_status("Loading dataset splits...")
        train_features = np.load("features_train.npy", allow_pickle=True)
        train_scores = np.load("scores_train.npy", allow_pickle=True)
        val_features = np.load("features_val.npy", allow_pickle=True)
        val_scores = np.load("scores_val.npy", allow_pickle=True)
        test_features = np.load("features_test.npy", allow_pickle=True)
        test_scores = np.load("scores_test.npy", allow_pickle=True)
        
        log_status(f"Train samples: {len(train_features)}", "INFO")
        log_status(f"Val samples: {len(val_features)}", "INFO")
        log_status(f"Test samples: {len(test_features)}", "INFO")
        
        log_status("Starting model training (50 epochs)...", "INFO")
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
        log_status("[OK] Training complete", "OK")
        
        log_status("Evaluating on test set...")
        test_metrics = evaluate_model(
            result["amfn"],
            result["temporal"],
            test_features,
            test_scores,
            device="cpu"
        )
        log_status("[OK] Evaluation complete", "OK")
        
        return result, test_metrics
    except Exception as e:
        log_status(f"Training failed: {str(e)}", "ERROR")
        return None, None

def run_inference():
    log_section("STEP 3: INFERENCE & EVALUATION")
    log_status("Running model inference on sample video...")
    
    try:
        from inference.run_inference import run_inference
        import os
        
        # Find a test video
        video_path = "data/videos/sample_video6.mp4"
        if not os.path.exists(video_path):
            video_path = None
            for f in os.listdir("data/videos"):
                if f.endswith(".mp4"):
                    video_path = os.path.join("data/videos", f)
                    break
        
        if not video_path:
            log_status("No test video found", "WARN")
            return None
        
        log_status(f"Processing: {video_path}", "INFO")
        result = run_inference(video_path)
        log_status("[OK] Inference complete", "OK")
        
        return result
    except Exception as e:
        log_status(f"Inference failed: {str(e)}", "ERROR")
        return None

def generate_report(training_result, test_metrics, inference_result):
    log_section("STEP 4: RESULTS REPORT")
    
    report = {
        "timestamp": datetime.now().isoformat(),
        "system": "AI Public Speaking Coach with CREMA-D Integration",
        "dataset_info": {
            "source": "data/videos + data/crema-d/VideoMP4",
            "sampling_strategy": "Smart CREMA-D sampling (1/300)",
            "total_videos": "~37 samples",
            "splits": {"train": "70%", "val": "15%", "test": "15%"}
        },
        "training_metrics": {
            "epochs": 50,
            "optimizer": "Adam",
            "learning_rate": 1e-3,
            "device": "CPU"
        },
        "test_results": test_metrics if test_metrics else "Not available",
        "inference_sample": inference_result if inference_result else "Not available"
    }
    
    # Save report
    report_path = "FINAL_RESULTS.json"
    with open(report_path, "w") as f:
        json.dump(report, f, indent=2)
    
    log_status(f"Report saved to {report_path}", "OK")
    
    # Print summary
    print("\n" + "="*70)
    print("  EXECUTION SUMMARY")
    print("="*70)
    print(json.dumps(report, indent=2))
    
    return report

def main():
    log_section("AI PUBLIC SPEAKING COACH - FULL PIPELINE EXECUTION")
    log_status(f"Starting at {datetime.now()}")
    
    # Step 1: Dataset Preparation
    splits, features, scores = run_dataset_preparation()
    
    # Step 2: Training
    training_result, test_metrics = run_training()
    
    # Step 3: Inference
    inference_result = run_inference()
    
    # Step 4: Report Generation
    report = generate_report(training_result, test_metrics, inference_result)
    
    log_section("PIPELINE EXECUTION COMPLETE")
    log_status(f"Finished at {datetime.now()}", "OK")

    if __name__ == "__main__":
        main()

if __name__ == "__main__":
    main()
