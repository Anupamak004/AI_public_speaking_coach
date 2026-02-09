import os
import csv
import numpy as np

from main import run_video_pipeline
from extract_audio_features import run_audio_pipeline
from filler_count.src.main import run_text_pipeline

# --------------------------------------------------
# PATHS
# --------------------------------------------------
ROOT = os.path.dirname(os.path.abspath(__file__))
CREMAD_VIDEO_DIR = os.path.join(ROOT, "data", "crema-d", "VideoMP4")
CSV_PATH = os.path.join(ROOT, "crema_d_fusion_scores.csv")

# --------------------------------------------------
# EMOTION → SCORE MAP (OUT OF 10)
# --------------------------------------------------
EMOTION_SCORE_MAP = {
    "HAP": {"confidence": 8, "clarity": 7, "fluency": 8, "engagement": 8, "nervousness": 2},
    "NEU": {"confidence": 6, "clarity": 6, "fluency": 6, "engagement": 5, "nervousness": 4},
    "SAD": {"confidence": 4, "clarity": 5, "fluency": 5, "engagement": 4, "nervousness": 6},
    "ANG": {"confidence": 5, "clarity": 6, "fluency": 6, "engagement": 6, "nervousness": 5},
    "FEA": {"confidence": 3, "clarity": 4, "fluency": 4, "engagement": 4, "nervousness": 8},
    "DIS": {"confidence": 4, "clarity": 5, "fluency": 5, "engagement": 4, "nervousness": 6},
}

# --------------------------------------------------
# CREATE CSV HEADER ONCE
# --------------------------------------------------
csv_initialized = False
processed_count = 0
MAX_VIDEOS = 10

for file in sorted(os.listdir(CREMAD_VIDEO_DIR)):
    if processed_count >= MAX_VIDEOS:
        print("\n🛑 Reached limit of 10 videos. Stopping.")
        break

    if not file.endswith(".mp4"):
        continue

    video_path = os.path.join(CREMAD_VIDEO_DIR, file)

    try:
        print(f"\n▶ Processing ({processed_count + 1}/10):", file)

        # -------- FEATURE EXTRACTION --------
        video_out = run_video_pipeline(video_path)
        audio_out = run_audio_pipeline(video_path)
        text_out  = run_text_pipeline(video_path)

        video_vec = video_out["video_vector"]
        audio_vec = audio_out["audio_vector"]
        text_vec  = text_out["text_vector"]

        fusion_vec = np.concatenate([video_vec, audio_vec, text_vec])

        # -------- CSV HEADER (ON FIRST VIDEO) --------
        if not csv_initialized:
            header = (
                ["file"]
                + [f"fusion_{i}" for i in range(len(fusion_vec))]
                + ["confidence", "clarity", "fluency", "engagement", "nervousness"]
            )

            with open(CSV_PATH, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow(header)

            csv_initialized = True
            print("📝 CSV initialized")

        # -------- LABEL FROM FILE NAME --------
        emotion_code = file.split("_")[2]

        scores = EMOTION_SCORE_MAP.get(
            emotion_code,
            {"confidence": 5, "clarity": 5, "fluency": 5, "engagement": 5, "nervousness": 5}
        )

        row = (
            [file]
            + fusion_vec.tolist()
            + list(scores.values())
        )

        # -------- WRITE ROW IMMEDIATELY --------
        with open(CSV_PATH, "a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(row)

        processed_count += 1
        print("✅ Written to CSV")

    except Exception as e:
        print("❌ Skipped:", file)
        print("   Reason:", e)

print(f"\n🎉 Done. Processed {processed_count} videos.")
print("📄 CSV saved at:", CSV_PATH)
