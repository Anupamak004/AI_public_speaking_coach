import textstat

def readability_features(text):
    return {
        "readability_score": textstat.flesch_reading_ease(text),
        "flesch_kincaid": textstat.flesch_kincaid_grade(text),
        "gunning_fog": textstat.gunning_fog(text)
    }
