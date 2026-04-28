def analyze_marks(marks):
    weak = []
    strong = []

    for subject, score in marks.items():
        score = int(score)

        if score < 50:
            weak.append(subject)
        elif score > 75:
            strong.append(subject)

    advice = []

    if weak:
        advice.append(f"Focus more on: {', '.join(weak)}")

    if strong:
        advice.append(f"Strong in: {', '.join(strong)}")

    if not weak:
        advice.append("Excellent performance! Keep it up.")

    return {
        "weak": weak,
        "strong": strong,
        "advice": advice
    }