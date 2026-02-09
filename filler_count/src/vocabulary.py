from nltk.tokenize import word_tokenize
import nltk
nltk.download('punkt', quiet=True)

def vocabulary_features(text):
    words = [w.lower() for w in word_tokenize(text) if w.isalpha()]
    unique_words = set(words)

    lexical_diversity = len(unique_words) / max(len(words), 1)
    repetition_rate = 1 - lexical_diversity

    return {
        "lexical_diversity": lexical_diversity,
        "repetition_rate": repetition_rate
    }
