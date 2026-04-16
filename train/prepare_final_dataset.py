import os
import sys
import numpy as np
import pandas as pd
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
CHALEARN_CSV = "data/chalearn_dataset.csv"
CHALEARN_VIDEO_DIR = "data/training80"
OUTPUT_FEATURES_FILE = "features_final.npy"
OUTPUT_SCORES_FILE = "scores_final.npy"

# Emotion-to-score mapping for CREMA-D
EMOTION_SCORE = {
    "ANG": [2, 2, 2, 1, 9],
    "FEA": [2, 2, 2, 2, 9],
    "SAD": [3, 3, 2, 3, 8],
    "HAP": [8, 8, 8, 8, 2],
    "DIS": [2, 2, 2, 2, 8],
    "NEU": [5, 5, 5, 5, 5],
}

# Custom video scores
VIDEO_SCORES = {
    "v1.mp4":  [4, 3, 3, 6, 7],
    "v2.mp4":  [3, 4, 3, 5, 9],
    "v3.mp4":  [2, 3, 3, 4, 8],
    "v4.mp4":  [4, 4, 3, 4, 8],
    "v5.mp4":  [4, 3, 3, 4, 9],
    "v6.mp4":  [1, 2, 3, 2, 8],
    "v7.mp4":  [6, 5, 5, 4, 4],
    "v8.mp4":  [8, 8, 9, 7, 2],
    "v9.mp4":  [9, 9, 9,7, 1],
    "v10.mp4": [8, 9, 8, 8, 2],
    "v11.mp4": [7, 8, 7, 6, 3],
    "v12.mp4": [8, 8, 9, 8, 1],
}

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

def process_video_quick(video_path, video_name, score):
    """Quick processing without caching for final dataset."""
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

        return (segment_data, score)

    except Exception as e:
        print(f"[ERROR] {video_name}: {str(e)}")
        return None

def build_final_dataset():
    features_list = []
    scores_list = []

    # Process custom videos
    print("Processing custom videos...")
    for video_name in sorted(os.listdir(VIDEO_DIR)):
        if not video_name.lower().endswith(".mp4"):
            continue

        video_path = os.path.join(VIDEO_DIR, video_name)
        if not os.path.exists(video_path):
            continue

        score = VIDEO_SCORES.get(video_name, [5, 5, 5, 5, 5])
        print(f"  {video_name}")

        result = process_video_quick(video_path, video_name, score)
        if result:
            segment_data, score_val = result
            features_list.append(segment_data)
            scores_list.append(np.asarray(score_val, dtype=np.float32))

    # Process CREMA-D (sample every 20th video for efficiency)
    print("Processing CREMA-D videos...")
    crema_videos = sorted([f for f in os.listdir(CREMA_VIDEO_DIR) if f.lower().endswith(".mp4")])
    sample_rate = max(1, len(crema_videos) // 200)  # ~200 CREMA-D videos

    for idx, video_name in enumerate(crema_videos):
        if idx % sample_rate != 0:
            continue

        video_path = os.path.join(CREMA_VIDEO_DIR, video_name)
        if not os.path.exists(video_path):
            continue

        score = get_score_for_crema_video(video_name)
        print(f"  {video_name} ({extract_emotion_from_crema_filename(video_name)})")

        result = process_video_quick(video_path, video_name, score)
        if result:
            segment_data, score_val = result
            features_list.append(segment_data)
            scores_list.append(np.asarray(score_val, dtype=np.float32))

    # Process ChaLearn videos
    print("Processing ChaLearn videos...")
    if os.path.exists(CHALEARN_CSV):
        df = pd.read_csv(CHALEARN_CSV)
        sample_size = min(300, len(df))  # Sample 300 ChaLearn videos
        df_sample = df.sample(n=sample_size, random_state=42)

        for idx, row in df_sample.iterrows():
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
            print(f"  {video_name}")

            result = process_video_quick(video_path, video_name, score)
            if result:
                segment_data, score_val = result
                features_list.append(segment_data)
                scores_list.append(np.asarray(score_val, dtype=np.float32))

    return np.array(features_list, dtype=object), np.array(scores_list, dtype=np.float32)

if __name__ == "__main__":
    print("Building final comprehensive dataset...")
    features, scores = build_final_dataset()

    print(f"Dataset built: {len(features)} videos")

    np.save(OUTPUT_FEATURES_FILE, features)
    np.save(OUTPUT_SCORES_FILE, scores)

    print(f"Saved to {OUTPUT_FEATURES_FILE} and {OUTPUT_SCORES_FILE}")
    print("Ready for training!")