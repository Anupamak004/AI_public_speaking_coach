import json
import os
import numpy as np


def _to_py(obj):
    if isinstance(obj, np.generic):
        return obj.item()
    if isinstance(obj, dict):
        return {k: _to_py(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [_to_py(v) for v in obj]
    return obj


class FeedbackGenerator:
    """
    Generates:
    - analysis.json  → quantitative + derived metrics
    - feedback.json  → qualitative feedback & suggestions ONLY
    """

    def __init__(self, output_dir):
        self.output_dir = output_dir

    # -------------------------------------------------
    def calculate_scores(self, stats):
        """
        Internal use ONLY (not written to feedback.json)
        """
        blink_rate = float(stats.get("blink_rate_per_min", 0.0))
        eye_contact = stats.get("gaze_distribution", {}).get("Center", 0)

        nervousness = min(100, int(blink_rate * 1.2))
        confidence = max(0, 100 - nervousness)
        engagement = 70 if eye_contact > 80 else 50

        return {
            "confidence": confidence,
            "engagement": engagement,
            "nervousness": nervousness
        }

    # -------------------------------------------------
    def generate_report(self, stats):
        """
        ✅ Writes FULL analysis to analysis.json
        """
        scores = self.calculate_scores(stats)

        analysis = {
            "video_duration_sec": stats.get("video_duration_sec", 0.0),
            "emotion_distribution": stats.get("emotion_distribution", {}),
            "eye_contact_score": stats.get("gaze_distribution", {}).get("Center", 0) / 100,
            "gaze_distribution": stats.get("gaze_distribution", {}),
            "blink_rate_per_min": stats.get("blink_rate_per_min", 0.0),
            "total_blinks": stats.get("total_blinks", 0),
            "head_pose": stats.get("head_pose", {}),
            "gestures": stats.get("gestures", {}),
            "final_scores": scores   # stays ONLY in analysis.json
        }

        analysis = _to_py(analysis)

        os.makedirs(self.output_dir, exist_ok=True)
        with open(os.path.join(self.output_dir, "analysis.json"), "w") as f:
            json.dump(analysis, f, indent=2)

    # -------------------------------------------------
    def generate_text_feedback(self, scores):
        """
        ✅ Writes ONLY qualitative feedback to feedback.json
        ❌ No scores
        ❌ No feedback.txt
        """
        feedback = {
            "feedback": self._generate_feedback(scores),
            "suggestions": self._generate_suggestions(scores)
        }

        feedback = _to_py(feedback)

        with open(os.path.join(self.output_dir, "feedback.json"), "w") as f:
            json.dump(feedback, f, indent=2)

    # -------------------------------------------------
    def _generate_feedback(self, scores):
        """
        Human-readable feedback (no numbers)
        """
        feedback = []

        if scores["confidence"] >= 75:
            feedback.append(
                "You appear confident while speaking and maintain good control over your delivery."
            )
        else:
            feedback.append(
                "Your confidence can be improved by maintaining steady posture and clearer voice projection."
            )

        if scores["engagement"] >= 65:
            feedback.append(
                "Your eye contact and presence help keep the audience engaged."
            )
        else:
            feedback.append(
                "Try increasing audience engagement through more expressive gestures and facial expressions."
            )

        if scores["nervousness"] > 60:
            feedback.append(
                "Signs of nervousness were observed during the speech."
            )
        else:
            feedback.append(
                "You appeared calm and composed throughout most of the speech."
            )

        return feedback

    # -------------------------------------------------
    def _generate_suggestions(self, scores):
        """
        Actionable improvement tips
        """
        suggestions = []

        if scores["nervousness"] > 60:
            suggestions.append(
                "Practice deep breathing and pause briefly between sentences to reduce nervousness."
            )

        if scores["confidence"] < 70:
            suggestions.append(
                "Stand upright, slow your speech slightly, and emphasize key points to build confidence."
            )

        if scores["engagement"] < 70:
            suggestions.append(
                "Use more natural hand gestures and vary your tone to make the speech more engaging."
            )

        if not suggestions:
            suggestions.append(
                "Excellent delivery overall. Continue practicing to maintain this level of performance."
            )

        return suggestions
