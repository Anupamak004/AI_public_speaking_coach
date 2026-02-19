def score_level(score):
    if score <= 3:
        return "poor"
    elif score <= 6:
        return "average"
    elif score <= 8:
        return "good"
    else:
        return "excellent"


FEEDBACK_RULES = {
    "Confidence": {
        "poor": "You appear hesitant and unsure while speaking.",
        "average": "Your confidence is moderate but can be improved.",
        "good": "You speak confidently most of the time.",
        "excellent": "You demonstrate excellent confidence and authority."
    },
    "Clarity": {
        "poor": "Your ideas are hard to follow and lack structure.",
        "average": "Your message is understandable but not very crisp.",
        "good": "Your points are clear and well-articulated.",
        "excellent": "Your speech is extremely clear and easy to follow."
    },
    "Fluency": {
        "poor": "Frequent pauses and breaks affect your flow.",
        "average": "You speak fluently at times, but with noticeable pauses.",
        "good": "Your speech flows smoothly with minimal hesitation.",
        "excellent": "You speak very fluently with natural pacing."
    },
    "Engagement": {
        "poor": "Your delivery does not engage the audience much.",
        "average": "Your engagement level is moderate.",
        "good": "You keep the audience engaged for most of the talk.",
        "excellent": "You are highly engaging and expressive."
    },
    "Nervousness": {
        "poor": "You appear very calm and composed.",
        "average": "You remain mostly calm while speaking.",
        "good": "Some nervousness is noticeable.",
        "excellent": "You appear very nervous while speaking."
    }
}


SUGGESTIONS = {
    "Confidence": "Practice speaking louder, maintain eye contact, and avoid filler words.",
    "Clarity": "Organize your points before speaking and slow down slightly.",
    "Fluency": "Practice speaking without scripts and work on reducing pauses.",
    "Engagement": "Use hand gestures, vary your tone, and ask rhetorical questions.",
    "Nervousness": "Take deep breaths before speaking and practice mock sessions."
}


def generate_feedback(scores: dict):
    feedback = {}
    suggestions = []

    for metric, score in scores.items():
        level = score_level(score)
        feedback[metric] = FEEDBACK_RULES[metric][level]

        # Add suggestion only if score is not good/excellent
        if score <= 6:
            suggestions.append(SUGGESTIONS[metric])

    return {
        "feedback": feedback,
        "suggestions": list(set(suggestions))  # remove duplicates
    }
