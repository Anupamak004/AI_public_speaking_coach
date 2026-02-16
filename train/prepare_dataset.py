import os
import sys
import numpy as np

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
OUTPUT_FEATURES_FILE = "features.npy"
OUTPUT_SCORES_FILE = "scores.npy"

# Manually provided scores (0–10 scale)
# [confidence, clarity, fluency, engagement, nervousness]
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

# -------------------------------------------------
# DATASET PREPARATION
# -------------------------------------------------
features_list = []
scores_list = []

for video_name, score in VIDEO_SCORES.items():
    video_path = os.path.join(VIDEO_DIR, video_name)

    if not os.path.exists(video_path):
        print(f"⚠️ Skipping missing file: {video_name}")
        continue

    print(f"\nProcessing {video_name}...")

    # -------- Segment video (ONLY to know number of segments) --------
    segments = segment_video(video_path, window_size=5)
    print(f"Segments: {len(segments)}")

    # -------- Extract features ONCE per video --------
    video_res = run_video_pipeline(video_path)
    audio_res = run_audio_pipeline(video_path)
    text_res  = run_text_pipeline(video_path)

    audio_vec = np.asarray(audio_res["audio_vector"], dtype=np.float32)
    video_vec = np.asarray(video_res["video_vector"], dtype=np.float32)
    text_vec  = np.asarray(text_res["text_vector"], dtype=np.float32)

    # -------- Build per-segment data --------
    segment_data = []
    for _ in segments:
        segment_data.append([
            audio_vec,
            video_vec,
            text_vec
        ])

    features_list.append(segment_data)
    scores_list.append(np.asarray(score, dtype=np.float32))

# -------------------------------------------------
# SAVE DATASET
# -------------------------------------------------
np.save(OUTPUT_FEATURES_FILE, np.array(features_list, dtype=object))
np.save(OUTPUT_SCORES_FILE, np.array(scores_list, dtype=np.float32))

print("\n✅ Dataset preparation complete!")
print(f"Saved features to: {OUTPUT_FEATURES_FILE}")
print(f"Saved scores   to: {OUTPUT_SCORES_FILE}")

# -------------------------------------------------
# SANITY CHECK
# -------------------------------------------------
print("\n--- Sanity Check ---")
print("Videos:", len(features_list))
print("Example video segments:", len(features_list[0]))
print("Audio dim:", features_list[0][0][0].shape)
print("Video dim:", features_list[0][0][1].shape)
print("Text dim :", features_list[0][0][2].shape)
print("Score example:", scores_list[0])
