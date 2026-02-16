import numpy as np

class FeedbackGenerator:
    """
    Converts predicted scores into textual feedback
    """

    metrics = ["Confidence", "Fluency", "Engagement", "Clarity", "Nervousness"]

    def __init__(self, score_scale=100):
        self.scale = score_scale

    def generate_feedback(self, scores):
        """
        scores: np.array of shape (5,) between 0-1
        returns: dict of scores (0-100) and textual feedback
        """
        scaled_scores = (scores * self.scale).round(1)
        feedback = []

        for metric, score in zip(self.metrics, scaled_scores):
            if metric != "Nervousness":
                if score > 80:
                    fb = f"Excellent {metric.lower()}!"
                elif score > 60:
                    fb = f"Good {metric.lower()}, minor improvements possible."
                else:
                    fb = f"{metric} needs improvement."
            else:  # Nervousness: lower is better
                if score < 20:
                    fb = "Very calm and composed."
                elif score < 50:
                    fb = "Some nervousness detected."
                else:
                    fb = "High nervousness, work on calming techniques."
            feedback.append(fb)

        return {
            "scores": dict(zip(self.metrics, scaled_scores)),
            "feedback": feedback
        }
