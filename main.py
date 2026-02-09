import argparse
import os
import sys
import logging

# Make src importable
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

from src.video_reader import VideoReader
from src.face_analysis import FaceAnalysis
from src.emotion_analysis import EmotionAnalysis
from src.eye_gaze import EyeGazeAnalysis
from src.pose_gesture import PoseGestureAnalysis
from src.aggregator import Aggregator
from src.feedback_generator import FeedbackGenerator
from src.fusion_vector import build_fusion_vector

# Logging
logging.basicConfig(level=logging.INFO, format="%(message)s")
logger = logging.getLogger(__name__)


# =========================================================
# ✅ REUSABLE VIDEO PIPELINE (FOR MULTIMODAL FUSION)
# =========================================================
def run_video_pipeline(video_path, output_dir="outputs"):
    if not os.path.exists(video_path):
        raise FileNotFoundError(f"Video not found: {video_path}")

    # ---------------- VIDEO READER ----------------
    reader = VideoReader(video_path, target_fps=15)

    info = reader.get_info()
    video_duration_sec = info["duration_sec"]

    # ---------------- ANALYZERS ----------------
    face_analyzer = FaceAnalysis()
    emotion_analyzer = EmotionAnalysis()
    eye_analyzer = EyeGazeAnalysis()
    pose_analyzer = PoseGestureAnalysis()

    # ---------------- AGGREGATOR ----------------
    aggregator = Aggregator()

    # ---------------- CALIBRATION ----------------
    CALIBRATION_FRAMES = 30
    calibration_ratios = []
    calibration_data = None
    calibration_done = False

    # ---------------- FRAME LOOP ----------------
    for frame_idx, frame in reader.get_frames():
        frame_result = {}

        # ---- FACE ----
        face_res = face_analyzer.analyze(frame)
        frame_result["face_detected"] = face_res["face_detected"]

        if face_res["face_detected"]:
            frame_result["head_pose"] = face_res["head_pose"]

            # ---- EYE / GAZE ----
            gaze_res = eye_analyzer.analyze(
                face_res["landmarks"],
                frame.shape,
                calibration_data=calibration_data
            )
            frame_result["gaze"] = gaze_res

            # ---- CALIBRATION ----
            if not calibration_done and gaze_res:
                calibration_ratios.append(gaze_res["raw_ratio"])
                if len(calibration_ratios) >= CALIBRATION_FRAMES:
                    baseline = sum(calibration_ratios) / len(calibration_ratios)
                    calibration_data = {"iris_ratio": baseline}
                    calibration_done = True

        # ---- EMOTION (1 FPS equivalent) ----
        if frame_idx % 15 == 0:
            em_res = emotion_analyzer.analyze(frame)
            if em_res:
                frame_result["emotion"] = em_res

        # ---- POSE ----
        pose_res = pose_analyzer.analyze(frame)
        frame_result["pose"] = pose_res

        # ---- AGGREGATE ----
        aggregator.add_frame_result(frame_idx, frame_result)

    # ---------------- FINAL METRICS ----------------
    eye_metrics = eye_analyzer.get_final_metrics(video_duration_sec)
    stats = aggregator.get_aggregated_stats()

    fusion_vector = build_fusion_vector(stats)

    # 🔒 SINGLE SOURCE OF TRUTH
    stats["video_duration_sec"] = eye_metrics["video_duration_sec"]
    stats["blink_rate_per_min"] = eye_metrics["blink_rate_per_min"]
    stats["total_blinks"] = eye_metrics["total_blinks"]

    return {
        "video_vector": fusion_vector,
        "video_stats": stats
    }


# =========================================================
# ✅ CLI ENTRY POINT (UNCHANGED USER EXPERIENCE)
# =========================================================
def main():
    parser = argparse.ArgumentParser(description="Public Speaking Video Analysis")
    parser.add_argument("--video", required=True, help="Path to input video")
    parser.add_argument("--output_dir", default="outputs", help="Output directory")
    args = parser.parse_args()

    logger.info("Starting analysis pipeline...")
    result = run_video_pipeline(args.video, args.output_dir)

    logger.info(
        f"FUSION VECTOR ({len(result['video_vector'])} dims): "
        f"{result['video_vector']}"
    )

    # ---------------- REPORT ----------------
    feedback_gen = FeedbackGenerator(args.output_dir)
    feedback_gen.generate_report(result["video_stats"])
    feedback_gen.generate_text_feedback(
        feedback_gen.calculate_scores(result["video_stats"])
    )

    logger.info(f"Analysis complete. Results saved to '{args.output_dir}'")


if __name__ == "__main__":
    main()
