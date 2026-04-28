TRANSLATIONS = {
    "Hello! I'm your study assistant.": {
        "kn": "ನಮಸ್ಕಾರ! ನಾನು ನಿಮ್ಮ ಅಧ್ಯಯನ ಸಹಾಯಕನು.",
        "hi": "नमस्ते! मैं आपका अध्ययन सहायक हूँ।"
    }
}

def translate_text(text, lang):
    if lang == "en":
        return text

    if text in TRANSLATIONS and lang in TRANSLATIONS[text]:
        return TRANSLATIONS[text][lang]

    return text