import numpy as np
from scipy.spatial import distance as dist


class EyeGazeAnalysis:
    """
    Authoritative Eye Blink & Gaze Analyzer
    """

    def __init__(self):
        self.EAR_THRESHOLD = 0.27
        self.MIN_CLOSED_FRAMES = 1

        self.closed_frames = 0
        self.prev_eye_closed = False
        self.total_blinks = 0

        self.LEFT_EYE = [362, 385, 387, 263, 373, 380]
        self.RIGHT_EYE = [33, 160, 158, 133, 153, 144]
        self.IRIS_CENTER = 473

    def _calculate_ear(self, eye):
        A = dist.euclidean(eye[1], eye[5])
        B = dist.euclidean(eye[2], eye[4])
        C = dist.euclidean(eye[0], eye[3])
        return (A + B) / (2.0 * C) if C else 0.0

    def analyze(self, landmarks, frame_shape, calibration_data=None):
        h, w, _ = frame_shape

        def px(i):
            lm = landmarks[i]
            return (int(lm[0] * w), int(lm[1] * h))

        left = [px(i) for i in self.LEFT_EYE]
        right = [px(i) for i in self.RIGHT_EYE]

        ear = (self._calculate_ear(left) + self._calculate_ear(right)) / 2.0
        closed = ear < self.EAR_THRESHOLD

        if closed:
            self.closed_frames += 1
        else:
            if self.prev_eye_closed and self.closed_frames >= self.MIN_CLOSED_FRAMES:
                self.total_blinks += 1
            self.closed_frames = 0

        self.prev_eye_closed = closed

        gaze = "Center"
        raw_ratio = 0.5

        if len(landmarks) > self.IRIS_CENTER:
            inner = np.array(px(362))
            outer = np.array(px(263))
            iris = np.array(px(self.IRIS_CENTER))
            width = np.linalg.norm(outer - inner)

            if width > 0:
                raw_ratio = float(np.linalg.norm(iris - inner) / width)
                baseline = calibration_data.get("iris_ratio", 0.5) if calibration_data else 0.5
                if raw_ratio < baseline - 0.08:
                    gaze = "Right"
                elif raw_ratio > baseline + 0.08:
                    gaze = "Left"

        return {
            "is_blinking": closed,
            "direction": gaze,
            "raw_ratio": float(raw_ratio)
        }

    # ✅ FINAL METRICS (VIDEO DURATION PASSED IN)
    def get_final_metrics(self, video_duration_sec):
        blink_rate = (self.total_blinks / video_duration_sec) * 60 if video_duration_sec > 0 else 0.0

        return {
            "video_duration_sec": float(video_duration_sec),
            "blink_rate_per_min": float(min(blink_rate, 60)),
            "total_blinks": int(self.total_blinks)
        }
