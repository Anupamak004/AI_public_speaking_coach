def build_fusion_vector(stats):
    vec = []

    # ---- VIDEO ----
    vec.append(stats.get("video_duration_sec", 0.0))

    # ---- EYE / GAZE ----
    vec.append(stats.get("eye_contact_score", 0.0))
    vec.append(stats.get("blink_rate_per_min", 0.0))

    gaze = stats.get("gaze_distribution", {})
    vec.append(gaze.get("Center", 0.0))
    vec.append(gaze.get("Left", 0.0))
    vec.append(gaze.get("Right", 0.0))

    # ---- HEAD POSE ----
    head_pose = stats.get("head_pose", {})
    movement = head_pose.get("movement_level", "0")
    movement_std = float(movement.split()[0]) if movement else 0.0
    vec.append(movement_std)

    # ---- EMOTIONS ----
    emotions = stats.get("emotion_distribution", {})
    for emo in ["angry", "disgust", "fear", "happy", "sad", "surprise", "neutral"]:
        vec.append(emotions.get(emo, 0.0))

    # ---- GESTURES ----
    gestures = stats.get("gestures", {})
    hand_usage_map = {"Low": 0.2, "Medium": 0.6, "High": 1.0}
    posture_map = {"Closed": 0.0, "Neutral": 0.5, "Open": 1.0}

    vec.append(hand_usage_map.get(gestures.get("hand_usage"), 0.0))
    vec.append(posture_map.get(gestures.get("posture"), 0.0))
    vec.append(1.0 if gestures.get("excessive_movement") else 0.0)

    # ---- FINAL SCORES ----
    scores = stats.get("final_scores", {})
    vec.append(scores.get("confidence", 0) / 100)
    vec.append(scores.get("engagement", 0) / 100)
    vec.append(scores.get("nervousness", 0) / 100)

    return vec
