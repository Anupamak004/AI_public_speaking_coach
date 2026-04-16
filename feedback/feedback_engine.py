import json

def score_level(score):
    if score <= 3:
        return "poor"
    elif score <= 6:
        return "average"
    elif score <= 8:
        return "good"
    else:
        return "excellent"


def generate_comprehensive_feedback(scores: dict, audio_features: dict = None, video_features: dict = None, text_features: dict = None):
    """
    Generate professional, realistic feedback incorporating scores and actual features
    Returns structured feedback with: overall_feedback, strengths, weaknesses, areas_to_improve
    """
    feedback_sections = {
        "overall_feedback": "",
        "strengths": [],
        "weaknesses": [],
        "areas_to_improve": []
    }

    # Extract feature data with defaults
    audio_stats = audio_features or {}
    video_stats = video_features or {}
    text_stats = text_features or {}

    # Audio-based analysis
    speech_rate = audio_stats.get("speech_rate", 0)
    pause_ratio = audio_stats.get("pause_ratio", 0)
    jitter = audio_stats.get("jitter", 0)
    shimmer = audio_stats.get("shimmer", 0)
    mean_pitch = audio_stats.get("librosa_mean_pitch", 0)
    pitch_variation = audio_stats.get("librosa_pitch_std", 0)

    # Video-based analysis
    eye_contact = video_stats.get("gaze_distribution", {}).get("Center", 0)
    blink_rate = video_stats.get("blink_rate_per_min", 0)
    emotion_dist = video_stats.get("emotion_distribution", {})
    head_stability = video_stats.get("head_pose", {}).get("stability", "Unknown")
    gestures = video_stats.get("gestures", {})

    # Text-based analysis
    readability = text_stats.get("readability_score", 0)
    words_per_min = text_stats.get("words_per_minute", 0)
    filler_count = text_stats.get("filler_count", 0)
    lexical_diversity = text_stats.get("lexical_diversity", 0)
    grammar_errors = text_stats.get("grammar_error_rate", 0)

    # Overall feedback based on scores
    confidence_score = scores.get("Confidence", 5)
    clarity_score = scores.get("Clarity", 5)
    fluency_score = scores.get("Fluency", 5)
    engagement_score = scores.get("Engagement", 5)
    nervousness_score = scores.get("Nervousness", 5)

    overall_score = (confidence_score + clarity_score + fluency_score + engagement_score + (10 - nervousness_score)) / 5

    if overall_score >= 8:
        feedback_sections["overall_feedback"] = "Excellent presentation overall! You demonstrated strong communication skills with effective delivery and audience engagement."
    elif overall_score >= 6:
        feedback_sections["overall_feedback"] = "Good presentation with solid foundation. With some refinements, you can elevate your speaking to the next level."
    elif overall_score >= 4:
        feedback_sections["overall_feedback"] = "Your presentation shows potential but needs work in several key areas to become more effective."
    else:
        feedback_sections["overall_feedback"] = "Your presentation requires significant improvement across multiple dimensions to be more impactful."

    # Strengths Analysis
    if confidence_score >= 7:
        feedback_sections["strengths"].append("Strong vocal confidence with steady delivery")
    elif eye_contact > 60 and blink_rate < 30:
        feedback_sections["strengths"].append("Good eye contact and composed demeanor")

    if clarity_score >= 7:
        feedback_sections["strengths"].append("Clear articulation and well-structured content")
    elif readability > 60:
        feedback_sections["strengths"].append("Readable and accessible language choices")

    if fluency_score >= 7:
        feedback_sections["strengths"].append("Smooth speech flow with natural pacing")
    elif speech_rate > 120 and speech_rate < 160:
        feedback_sections["strengths"].append("Appropriate speaking pace")

    if engagement_score >= 7:
        feedback_sections["strengths"].append("Engaging delivery that maintains audience attention")
    elif emotion_dist.get("happy", 0) > 20 or emotion_dist.get("surprise", 0) > 15:
        feedback_sections["strengths"].append("Positive emotional expression")

    if nervousness_score <= 3:
        feedback_sections["strengths"].append("Calm and composed throughout the presentation")
    elif blink_rate < 25:
        feedback_sections["strengths"].append("Relaxed facial expressions")

    if lexical_diversity > 0.7:
        feedback_sections["strengths"].append("Rich vocabulary and varied word choice")

    if filler_count == 0:
        feedback_sections["strengths"].append("Minimal use of filler words")

    # Weaknesses Analysis
    if confidence_score <= 4:
        feedback_sections["weaknesses"].append("Low vocal confidence affecting delivery impact")
    elif mean_pitch < 100 and pitch_variation < 30:
        feedback_sections["weaknesses"].append("Monotone delivery lacking vocal variety")

    if clarity_score <= 4:
        feedback_sections["weaknesses"].append("Unclear articulation making content hard to follow")
    elif grammar_errors > 0.1:
        feedback_sections["weaknesses"].append("Grammar issues affecting professionalism")

    if fluency_score <= 4:
        feedback_sections["weaknesses"].append("Frequent pauses disrupting speech flow")
    elif pause_ratio > 0.7:
        feedback_sections["weaknesses"].append("Excessive pausing reducing fluency")

    if engagement_score <= 4:
        feedback_sections["weaknesses"].append("Limited audience engagement and connection")
    elif eye_contact < 30:
        feedback_sections["weaknesses"].append("Poor eye contact with audience")

    if nervousness_score >= 7:
        feedback_sections["weaknesses"].append("Visible signs of nervousness affecting performance")
    elif blink_rate > 40:
        feedback_sections["weaknesses"].append("Frequent blinking indicating anxiety")

    if speech_rate < 100:
        feedback_sections["weaknesses"].append("Slow speaking pace that may bore audience")
    elif speech_rate > 180:
        feedback_sections["weaknesses"].append("Rapid speech making content hard to follow")

    if filler_count > 3:
        feedback_sections["weaknesses"].append(f"Frequent filler words ({filler_count} detected) reducing credibility")

    if lexical_diversity < 0.5:
        feedback_sections["weaknesses"].append("Limited vocabulary reducing expressiveness")

    # Areas to Improve
    if confidence_score <= 6:
        feedback_sections["areas_to_improve"].append("Practice vocal projection and maintain steady eye contact to build confidence")

    if clarity_score <= 6:
        feedback_sections["areas_to_improve"].append("Work on clear articulation and organize content with better structure")

    if fluency_score <= 6:
        feedback_sections["areas_to_improve"].append("Reduce pauses by practicing delivery and using transitional phrases")

    if engagement_score <= 6:
        feedback_sections["areas_to_improve"].append("Incorporate more gestures and vary your tone to increase audience engagement")

    if nervousness_score >= 5:
        feedback_sections["areas_to_improve"].append("Practice relaxation techniques and deep breathing to reduce visible anxiety")

    if speech_rate < 120 or speech_rate > 160:
        feedback_sections["areas_to_improve"].append("Adjust speaking pace to approximately 120-160 words per minute")

    if eye_contact < 50:
        feedback_sections["areas_to_improve"].append("Increase eye contact by looking at different audience sections")

    if filler_count > 0:
        feedback_sections["areas_to_improve"].append("Minimize filler words through conscious awareness and practice")

    if lexical_diversity < 0.6:
        feedback_sections["areas_to_improve"].append("Expand vocabulary and use more varied language")

    # Ensure we have at least one item in each section if empty
    if not feedback_sections["strengths"]:
        feedback_sections["strengths"].append("Presentation shows effort and willingness to communicate")

    if not feedback_sections["weaknesses"]:
        feedback_sections["weaknesses"].append("Areas for improvement exist but are manageable with practice")

    if not feedback_sections["areas_to_improve"]:
        feedback_sections["areas_to_improve"].append("Continue practicing to maintain and build upon current skills")

    return feedback_sections


# Updated function to provide comprehensive feedback
def generate_feedback(scores: dict, audio_features: dict = None, video_features: dict = None, text_features: dict = None):
    """
    Generate professional, realistic feedback incorporating scores and actual features
    Returns structured feedback with: overall_feedback, strengths, weaknesses, areas_to_improve
    """
    return generate_comprehensive_feedback(scores, audio_features, video_features, text_features)
