from flask import Flask, render_template, request, jsonify
from services.chatbot import chatbot_reply
from services.recommender import analyze_marks
from services.translator import translate_text

app = Flask(__name__)

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/resources')
def resources():
    return render_template("resources.html")

# Chatbot
@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.json
    msg = data.get("message", "")
    lang = data.get("lang", "en")

    reply = chatbot_reply(msg)
    translated = translate_text(reply, lang)

    return jsonify({"reply": translated})

# Recommendation
@app.route('/api/recommend', methods=['POST'])
def recommend():
    marks = request.json
    result = analyze_marks(marks)
    return jsonify(result)

# Translate any UI text
@app.route('/api/translate', methods=['POST'])
def translate():
    data = request.json
    return jsonify({
        "text": translate_text(data["text"], data["lang"])
    })

if __name__ == "__main__":
    app.run(debug=True)