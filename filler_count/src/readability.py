import textstat

def readability_features(text):
    print("🔹 Readability & Clarity")
    print("Flesch Reading Ease:", round(textstat.flesch_reading_ease(text), 2))
    print("Flesch-Kincaid Grade:", round(textstat.flesch_kincaid_grade(text), 2))
    print("Gunning Fog Index:", round(textstat.gunning_fog(text), 2))
    print()
