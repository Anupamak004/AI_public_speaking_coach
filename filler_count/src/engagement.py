import re
from nltk.tokenize import sent_tokenize

def engagement_features(text):
    print("🔹 Engagement Analysis")

    sentences = sent_tokenize(text)
    total_sentences = len(sentences)

    # --- Questions ---
    question_count = sum(1 for s in sentences if s.strip().endswith("?"))

    # --- Audience Address ---
    audience_words = [
        "you", "your", "we", "us", "our"
    ]
    audience_count = sum(text.lower().count(w) for w in audience_words)

    # --- Discourse Markers ---
    discourse_markers = [
        "first", "second", "next", "however",
        "therefore", "finally", "in conclusion"
    ]
    marker_count = sum(text.lower().count(m) for m in discourse_markers)

    # --- Storytelling Indicators ---
    story_words = [
        "imagine", "story", "example", "suppose",
        "let me tell", "once"
    ]
    story_count = sum(text.lower().count(w) for w in story_words)

    # --- Normalize ---
    question_rate = question_count / max(total_sentences, 1)

    print(f"Total sentences: {total_sentences}")
    print(f"Questions: {question_count}")
    print(f"Audience references: {audience_count}")
    print(f"Discourse markers: {marker_count}")
    print(f"Storytelling cues: {story_count}")

    # --- Engagement Score ---
    score = (
        question_rate * 3 +
        marker_count * 0.5 +
        story_count * 1 +
        audience_count * 0.2
    )

    print(f"Engagement score: {round(score, 2)}")

    # --- Verdict ---
    if score > 5:
        print("🔥 Highly engaging speech")
    elif score > 2:
        print("✅ Moderately engaging speech")
    else:
        print("⚠ Low engagement (needs interaction)")

    print()
