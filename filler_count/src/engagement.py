import re
from nltk.tokenize import sent_tokenize

def engagement_features(text):
    sentences = sent_tokenize(text)
    total_sentences = len(sentences)

    # Questions
    question_count = sum(1 for s in sentences if s.strip().endswith("?"))

    # Audience address
    audience_words = ["you", "your", "we", "us", "our"]
    audience_count = sum(text.lower().count(w) for w in audience_words)

    # Discourse markers
    discourse_markers = ["first", "second", "next", "however", "therefore", "finally", "in conclusion"]
    marker_count = sum(text.lower().count(m) for m in discourse_markers)

    # Storytelling
    story_words = ["imagine", "story", "example", "suppose", "let me tell", "once"]
    story_count = sum(text.lower().count(w) for w in story_words)

    # Engagement score formula
    score = (
        (question_count / max(total_sentences, 1)) * 3 +
        marker_count * 0.5 +
        story_count * 1 +
        audience_count * 0.2
    )

    return {"engagement_score": score}
