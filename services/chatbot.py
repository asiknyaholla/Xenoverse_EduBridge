import random

RESPONSES = {
    "greeting": [
        "Hello! I'm your study assistant.",
        "Hi! How can I help you today?"
    ],
    "math": [
        "Practice formulas daily and solve previous papers.",
        "Focus on algebra and geometry basics."
    ],
    "science": [
        "Revise diagrams and key concepts.",
        "Focus on physics numericals and biology diagrams."
    ],
    "exam": [
        "Solve last 5 years question papers.",
        "Time management is key for exams."
    ],
}

def chatbot_reply(msg):
    msg = msg.lower()

    if any(word in msg for word in ["hi", "hello"]):
        return random.choice(RESPONSES["greeting"])

    if "math" in msg:
        return random.choice(RESPONSES["math"])

    if "science" in msg:
        return random.choice(RESPONSES["science"])

    if "exam" in msg:
        return random.choice(RESPONSES["exam"])

    return "I can help with subjects, exams, and study plans!"