import language_tool_python
tool = language_tool_python.LanguageTool('en-US')

def grammar_features(text):
    matches = tool.check(text)
    total_words = len(text.split())
    error_rate = len(matches) / max(total_words, 1)

    return {"grammar_error_rate": error_rate}
