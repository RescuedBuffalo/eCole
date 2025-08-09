def detect_intent(text: str) -> str:
    return "question" if "?" in text else "statement"


def detect_emotion(text: str) -> str:
    text_lower = text.lower()
    if "!" in text:
        return "excited"
    if any(word in text_lower for word in ["sad", "unhappy"]):
        return "sad"
    return "neutral"
