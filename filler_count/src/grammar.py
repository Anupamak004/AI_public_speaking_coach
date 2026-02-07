import language_tool_python

tool = language_tool_python.LanguageTool('en-US')

def grammar_features(text, max_examples=5):
    print("🔹 Grammar & Fluency Analysis")

    matches = tool.check(text)
    error_count = len(matches)
    total_words = len(text.split())

    error_rate = error_count / max(total_words, 1)

    print(f"Total grammar issues: {error_count}")
    print(f"Error rate: {round(error_rate, 3)}")

    # ---- FLUENCY JUDGMENT ----
    if error_rate > 0.05:
        print("⚠ Poor grammatical fluency")
    elif error_rate > 0.02:
        print("🟡 Moderate grammatical fluency")
    else:
        print("✅ Good grammatical fluency")

    # ---- PRINT ERROR DETAILS ----
    if error_count > 0:
        print("\n📌 Sample Grammar Issues (with suggestions):")

        for i, match in enumerate(matches[:max_examples], start=1):
            context = match.context
            error = match.message
            suggestions = match.replacements[:3]  # top 3 suggestions

            print(f"\n{i}. Issue: {error}")
            print(f"   Context: {context}")
            if suggestions:
                print(f"   Suggestions: {', '.join(suggestions)}")
            else:
                print("   Suggestions: No suggestion available")

    print()
