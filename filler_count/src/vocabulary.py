import nltk
from nltk.tokenize import word_tokenize

nltk.download('punkt')

def vocabulary_features(text):
    print("🔹 Vocabulary Richness")
    words = [w.lower() for w in word_tokenize(text) if w.isalpha()]
    unique_words = set(words)

    ttr = len(unique_words) / len(words) if words else 0
    repetition_rate = 1 - ttr

    print("Total words:", len(words))
    print("Unique words:", len(unique_words))
    print("Type-Token Ratio:", round(ttr, 3))
    print("Repetition Rate:", round(repetition_rate, 3))
    print()
