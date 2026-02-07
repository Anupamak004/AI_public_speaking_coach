from collections import defaultdict, deque
import numpy as np


class Aggregator:
    """
    Aggregates frame-level analysis into high-level behavioral summaries.
    """

    def __init__(self, smoothing_window=5):
        # ---- HEAD POSE ----
        self.pose_history = deque(maxlen=smoothing_window)
        self.head_scores = []

        # ---- EMOTIONS ----
        self.emotions = defaultdict(float)
        self.emotion_samples = 0

        # ---- GAZE ----
        self.gazes = defaultdict(int)

        # ---- GESTURES ----
        self.total_pose_frames = 0
        self.hand_visible_count = 0
        self.open_posture_count = 0

    # -------------------------------------------------
    def add_frame_result(self, frame_idx, res):
        # ---- HEAD POSE SMOOTHING ----
        if "head_pose" in res and res["head_pose"]:
            hp = res["head_pose"]
            self.pose_history.append((hp["yaw"], hp["pitch"]))

            hp["yaw"] = float(np.mean([p[0] for p in self.pose_history]))
            hp["pitch"] = float(np.mean([p[1] for p in self.pose_history]))

            self.head_scores.append(hp)

        # ---- EMOTIONS ----
        if "emotion" in res and res["emotion"]:
            for k, v in res["emotion"]["distribution"].items():
                self.emotions[k] += float(v)
            self.emotion_samples += 1

        # ---- GAZE ----
        if "gaze" in res and res["gaze"]:
            self.gazes[res["gaze"]["direction"]] += 1

        # ---- GESTURES / POSTURE ----
        if "pose" in res and res["pose"]:
            self.total_pose_frames += 1

            if res["pose"].get("hands_visible"):
                self.hand_visible_count += 1

            if res["pose"].get("posture_type") == "Open":
                self.open_posture_count += 1

    # -------------------------------------------------
    def get_aggregated_stats(self):
        # ---------- EMOTION DISTRIBUTION ----------
        emotion_dist = {}
        if self.emotion_samples > 0:
            total = sum(self.emotions.values())
            emotion_dist = {
                k: round((v / total) * 100, 1)
                for k, v in self.emotions.items()
            }

        # ---------- GAZE DISTRIBUTION ----------
        gaze_total = sum(self.gazes.values())
        gaze_dist = {
            k: round((v / gaze_total) * 100, 1)
            for k, v in self.gazes.items()
        } if gaze_total > 0 else {}

        # ---------- HEAD POSE SUMMARY ----------
        if self.head_scores:
            yaw_vals = [h["yaw"] for h in self.head_scores]
            movement = float(np.std(yaw_vals))

            if movement < 5:
                stability = "Good"
            elif movement < 10:
                stability = "Moderate"
            else:
                stability = "Poor"
        else:
            movement = 0.0
            stability = "Unknown"

        head_pose_summary = {
            "stability": stability,
            "movement_level": f"{movement:.2f} (std dev)"
        }

        # ---------- GESTURE SUMMARY ----------
        if self.total_pose_frames > 0:
            hand_ratio = self.hand_visible_count / self.total_pose_frames
            posture_ratio = self.open_posture_count / self.total_pose_frames

            hand_usage = (
                "High" if hand_ratio > 0.6
                else "Medium" if hand_ratio > 0.3
                else "Low"
            )

            posture = "Open" if posture_ratio > 0.6 else "Closed"
        else:
            hand_usage = "Unknown"
            posture = "Unknown"

        gestures = {
            "hand_usage": hand_usage,
            "posture": posture,
            "excessive_movement": movement > 12
        }

        return {
            "emotion_distribution": emotion_dist,
            "gaze_distribution": gaze_dist,
            "head_pose": head_pose_summary,
            "gestures": gestures
        }
