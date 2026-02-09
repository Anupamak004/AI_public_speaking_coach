def confidence_features(text):
    weak_words = [
        "maybe", "probably", "i think", "i guess",
        "kind of", "sort of", "possibly"
    ]
    strong_words = [
        "will", "must", "definitely", "clearly",
        "proven", "always", "never"
    ]

    text_lower = text.lower()
    weak_count = sum(text_lower.count(w) for w in weak_words)
    strong_count = sum(text_lower.count(w) for w in strong_words)

    # Confidence score: 0 to 1
    score = max(strong_count - weak_count, 0) / max(strong_count + weak_count, 1)

    return {"confidence_score": score}
