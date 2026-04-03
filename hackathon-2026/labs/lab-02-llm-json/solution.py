def summarize_text(text):
    # Simple title (first 5 words)
    words = text.split()
    title = " ".join(words[:5])

    # Create 3 summary points
    points = [
        " ".join(words[:len(words)//3]),
        " ".join(words[len(words)//3:2*len(words)//3]),
        " ".join(words[2*len(words)//3:])
    ]

    # Simple sentiment logic
    text_lower = text.lower()

    if "good" in text_lower or "improving" in text_lower or "transforming" in text_lower:
        sentiment = "positive"
    elif "bad" in text_lower or "problem" in text_lower:
        sentiment = "negative"
    else:
        sentiment = "neutral"

    return {
        "title": title,
        "points": points,
        "sentiment": sentiment
    }
