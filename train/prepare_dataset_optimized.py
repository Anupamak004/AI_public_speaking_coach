import os
import sys
import csv
import numpy as np
import pandas as pd
import random
from pathlib import Path

# -------------------------------------------------
# Path setup
# -------------------------------------------------
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(ROOT)

from sequence.segmenter import segment_video
from main import run_video_pipeline
from extract_audio_features import run_audio_pipeline
from filler_count.src.main import run_text_pipeline

# -------------------------------------------------
# CONFIG
# -------------------------------------------------
VIDEO_DIR = "data/videos"
CREMA_VIDEO_DIR = "data/crema-d/VideoMP4"
CREMA_CSV = "data/crema-d/finishedEmoResponses.csv"
CHALEARN_CSV = "data/chalearn_dataset.csv"
CHALEARN_VIDEO_DIR = "data/training80"
OUTPUT_FEATURES_FILE = "features_large.npy"
OUTPUT_SCORES_FILE = "scores_large.npy"
OUTPUT_SPLIT = {
    "train": ("features_train_large.npy", "scores_train_large.npy"),
    "val":   ("features_val_large.npy", "scores_val_large.npy"),
    "test":  ("features_test_large.npy", "scores_test_large.npy"),
}

# Emotion-to-public-speaking metric mapping (0–10 scale)
EMOTION_SCORE = {
    "ANG": [2, 2, 2, 1, 9],
    "FEA": [2, 2, 2, 2, 9],
    "SAD": [3, 3, 2, 3, 8],
    "HAP": [8, 8, 8, 8, 2],
    "DIS": [2, 2, 2, 2, 8],
    "NEU": [5, 5, 5, 5, 5],
}

# Add predefined video scores
VIDEO_SCORES = {
    "v1.mp4":  [4, 3, 3, 6, 7],
    "v2.mp4":  [3, 4, 3, 5, 9],
    "v3.mp4":  [2, 3, 3, 4, 8],
    "v4.mp4":  [4, 4, 3, 4, 8],
    "v5.mp4":  [4, 3, 3, 4, 9],
    "v6.mp4":  [1, 2, 3, 2, 8],
    "v7.mp4":  [6, 5, 5, 4, 4],
    "v8.mp4":  [8, 8, 9, 7, 2],
    "v9.mp4":  [9, 9, 9, 7, 1],
    "v10.mp4": [8, 9, 8, 8, 2],
    "v11.mp4": [7, 8, 7, 6, 3],
    "v12.mp4": [8, 8, 9, 8, 1],
}

TARGET_VIDEOS = 1000  # Target ~1000 videos

# -------------------------------------------------
# UTILITIES
# -------------------------------------------------

def parse_crema_scores(csv_path):
    if not os.path.exists(csv_path):
        return {}
    mapping = {}
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            clip = row.get("clipName", "").strip()
            if not clip:
                continue
            parts = clip.split("_")
            if len(parts) < 3:
                continue
            emotion_code = parts[-2]
            if emotion_code not in EMOTION_SCORE:
                emotion_code = parts[-1] if parts[-1] in EMOTION_SCORE else None
            if emotion_code in EMOTION_SCORE:
                mapping[clip] = EMOTION_SCORE[emotion_code]
    return mapping


def load_chalearn_data(csv_path):
    if not os.path.exists(csv_path):
        return pd.DataFrame()
    df = pd.read_csv(csv_path)
    return df


def get_score_for_video(video_name, crema_score_map):
    if video_name in VIDEO_SCORES:
        return VIDEO_SCORES[video_name]
    name_base = os.path.splitext(video_name)[0]
    cyf = crema_score_map.get(name_base)
    if cyf:
        return cyf
    return [5, 5, 5, 5, 5]


def extract_emotion_from_crema_filename(filename):
    name_base = os.path.splitext(filename)[0]
    parts = name_base.split("_")
    if len(parts) >= 3:
        for part in parts[-2:]:
            if part in EMOTION_SCORE:
                return part
    return None


def get_score_for_crema_video(filename):
    emotion = extract_emotion_from_crema_filename(filename)
    if emotion and emotion in EMOTION_SCORE:
        return EMOTION_SCORE[emotion]
    return [5, 5, 5, 5, 5]


def process_video_cached(video_path, video_name, score, cache_dir="video_cache"):
    """Process video with caching to avoid reprocessing."""
    os.makedirs(cache_dir, exist_ok=True)
    
    cache_file = os.path.join(cache_dir, f"{os.path.splitext(video_name)[0]}_cache.npy")
    
    if os.path.exists(cache_file):
        try:
            return np.load(cache_file, allow_pickle=True)
        except:
            pass
    
    try:
        segments = segment_video(video_path, window_size=5)
        if len(segments) == 0:
            return None

        video_res = run_video_pipeline(video_path)
        audio_res = run_audio_pipeline(video_path)
        text_res = run_text_pipeline(video_path)

        audio_vec = np.asarray(audio_res.get("audio_vector", []), dtype=np.float32)
        video_vec = np.asarray(video_res.get("video_vector", []), dtype=np.float32)
        text_vec = np.asarray(text_res.get("text_vector", []), dtype=np.float32)

        if audio_vec.size == 0 or video_vec.size == 0 or text_vec.size == 0:
            return None

        segment_data = []
        for _ in segments:
            segment_data.append([audio_vec, video_vec, text_vec])

        result = (segment_data, score)
        np.save(cache_file, np.array(result, dtype=object), allow_pickle=True)
        return result

    except Exception as e:
        print(f"[ERROR] Error processing {video_name}: {str(e)}")
        return None


# -------------------------------------------------
# DATASET PREPARATION
# -------------------------------------------------

def build_large_dataset():
    crema_score_map = parse_crema_scores(CREMA_CSV)
    chalearn_df = load_chalearn_data(CHALEARN_CSV)

    features_list = []
    scores_list = []
    processed_count = 0
    failed_count = 0

    # ========================================
    # PROCESS DATA/VIDEOS DIRECTORY
    # ========================================
    print("\n" + "="*60)
    print("[PHASE 1] Processing data/videos directory...")
    print("="*60)
    
    for video_name in sorted(os.listdir(VIDEO_DIR)):
        if processed_count >= TARGET_VIDEOS:
            break
        if not video_name.lower().endswith(".mp4"):
            continue

        video_path = os.path.join(VIDEO_DIR, video_name)
        if not os.path.exists(video_path):
            print(f"[WARN] Skipping missing file: {video_name}")
            continue

        score = get_score_for_video(video_name, crema_score_map)
        print(f"\n[{processed_count+1}] Processing {video_name}...")

        result = process_video_cached(video_path, video_name, score)
        if result:
            segment_data, score_val = result
            features_list.append(segment_data)
            scores_list.append(np.asarray(score_val, dtype=np.float32))
            processed_count += 1
            print(f"  ✓ Processed (total: {processed_count})")
        else:
            failed_count += 1
            print(f"  ✗ Failed (skipped)")

    print(f"\n[OK] Data/videos: Loaded {len(features_list)} videos / {failed_count} failed")

    # ========================================
    # PROCESS CREMA-D DIRECTORY
    # ========================================
    if processed_count < TARGET_VIDEOS:
        print("\n" + "="*60)
        print(f"[PHASE 2] Processing {CREMA_VIDEO_DIR} directory...")
        print("="*60)
        
        crema_videos = sorted([f for f in os.listdir(CREMA_VIDEO_DIR) if f.lower().endswith(".mp4")])
        total_crema = len(crema_videos)
        
        # Calculate sampling rate to reach target
        remaining = TARGET_VIDEOS - processed_count
        sample_rate = max(1, total_crema // remaining) if remaining > 0 else total_crema
        
        print(f"Found {total_crema} CREMA-D videos. Sampling 1 every {sample_rate}...")
        
        for idx, video_name in enumerate(crema_videos):
            if processed_count >= TARGET_VIDEOS:
                break
            if idx % sample_rate != 0:
                continue

            video_path = os.path.join(CREMA_VIDEO_DIR, video_name)
            if not os.path.exists(video_path):
                continue

            score = get_score_for_crema_video(video_name)
            emotion = extract_emotion_from_crema_filename(video_name)
            print(f"\n[{processed_count+1}] CREMA-D: {video_name} ({emotion})...")

            result = process_video_cached(video_path, video_name, score, cache_dir="crema_cache")
            if result:
                segment_data, score_val = result
                features_list.append(segment_data)
                scores_list.append(np.asarray(score_val, dtype=np.float32))
                processed_count += 1
                print(f"  ✓ Processed (total: {processed_count})")
            else:
                failed_count += 1
                print(f"  ✗ Failed (skipped)")

        print(f"\n[OK] CREMA-D: Loaded {len(features_list)-12} videos / {failed_count} failed")

    # ========================================
    # PROCESS CHALEARN DIRECTORY
    # ========================================
    if processed_count < TARGET_VIDEOS and not chalearn_df.empty and os.path.exists(CHALEARN_VIDEO_DIR):
        print("\n" + "="*60)
        print(f"[PHASE 3] Processing {CHALEARN_VIDEO_DIR} directory...")
        print("="*60)
        
        print(f"Found {len(chalearn_df)} ChaLearn videos. Sampling to reach {TARGET_VIDEOS} total...")
        
        remaining = TARGET_VIDEOS - processed_count
        if remaining > 0:
            chalearn_sample = chalearn_df.sample(n=min(remaining, len(chalearn_df)), random_state=42).reset_index(drop=True)
            
            for idx, row in chalearn_sample.iterrows():
                if processed_count >= TARGET_VIDEOS:
                    break
                    
                video_name = row['video']
                video_path = os.path.join(CHALEARN_VIDEO_DIR, video_name)
                
                if not os.path.exists(video_path):
                    continue
                
                score = [
                    row['confidence'],
                    row['clarity'], 
                    row['fluency'],
                    row['engagement'],
                    row['nervousness']
                ]
                
                print(f"\n[{processed_count+1}] ChaLearn: {video_name}...")

                result = process_video_cached(video_path, video_name, score, cache_dir="chalearn_cache")
                if result:
                    segment_data, score_val = result
                    features_list.append(segment_data)
                    scores_list.append(np.asarray(score_val, dtype=np.float32))
                    processed_count += 1
                    print(f"  ✓ Processed (total: {processed_count})")
                else:
                    failed_count += 1
                    print(f"  ✗ Failed (skipped)")

        print(f"\n[OK] ChaLearn: Loaded {processed_count - 12} videos total / {failed_count} failed")

    return np.array(features_list, dtype=object), np.array(scores_list, dtype=np.float32)


def split_dataset(features, scores, train_frac=0.7, val_frac=0.15, test_frac=0.15, random_seed=42):
    assert len(features) == len(scores), "Features and scores must match"
    n = len(features)

    indices = np.arange(n)
    np.random.seed(random_seed)
    np.random.shuffle(indices)

    n_train = int(n * train_frac)
    n_val = int(n * val_frac)

    train_idx = indices[:n_train]
    val_idx = indices[n_train:n_train + n_val]
    test_idx = indices[n_train + n_val:]

    splits = {
        "train": (features[train_idx], scores[train_idx]),
        "val": (features[val_idx], scores[val_idx]),
        "test": (features[test_idx], scores[test_idx]),
    }

    return splits


def save_splits(splits):
    for split_name, (feat, sc) in splits.items():
        ft_file, sc_file = OUTPUT_SPLIT[split_name]
        np.save(ft_file, feat)
        np.save(sc_file, sc)
        print(f"Saved {split_name} set: {ft_file} ({len(feat)}), {sc_file} ({len(sc)})")


if __name__ == "__main__":
    print(f"\n{'='*60}")
    print(f"LARGE DATASET PREPARATION (Target: ~{TARGET_VIDEOS} videos)")
    print(f"{'='*60}")
    
    features, scores = build_large_dataset()
    
    print(f"\n{'='*60}")
    print(f"[OK] DATASET BUILT: {len(features)} videos total")
    print(f"{'='*60}")

    splits = split_dataset(features, scores)
    
    print("\n--- Split Distribution ---")
    print(f"Train: {len(splits['train'][0])} videos ({splits['train'][0].shape[0]/len(features)*100:.1f}%)")
    print(f"Val:   {len(splits['val'][0])} videos ({splits['val'][0].shape[0]/len(features)*100:.1f}%)")
    print(f"Test:  {len(splits['test'][0])} videos ({splits['test'][0].shape[0]/len(features)*100:.1f}%)")
    
    save_splits(splits)

    np.save(OUTPUT_FEATURES_FILE, features)
    np.save(OUTPUT_SCORES_FILE, scores)

    print("\n--- Sanity Check ---")
    print("Total videos:", len(features))
    if len(features) > 0:
        print("Example segments:", len(features[0]) if len(features) else 0)
        print("Audio dim:", features[0][0][0].shape if len(features) > 0 else "N/A")
        print("Video dim:", features[0][0][1].shape if len(features) > 0 else "N/A")
        print("Text dim :", features[0][0][2].shape if len(features) > 0 else "N/A")
        print("Score example:", scores[0])
    
    print(f"\n✅ Dataset preparation complete! Files saved with '_large' suffix.")
