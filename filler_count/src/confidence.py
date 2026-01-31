def confidence_features(text):
    print("🔹 Confidence Analysis")

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

    print("Weak words count:", weak_count)
    print("Strong words count:", strong_count)

    if weak_count > strong_count:
        print("⚠ Speaker lacks confidence")
    else:
        print("✅ Speaker sounds confident")
    print()
