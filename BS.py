from flask import Flask, render_template, request, jsonify
import os

app = Flask(__name__)

# ── Page Routes ──────────────────────────────────────────────

@app.route('/')
@app.route('/index.html')
def index():
    return render_template('index.html')

@app.route('/resources.html')
def resources():
    return render_template('resources.html')

@app.route('/book-online.html')
def book_online():
    return render_template('book-online.html')

@app.route('/program-list.html')
def program_list():
    return render_template('program-list.html')

@app.route('/notifications.html')
def notifications():
    return render_template('notifications.html')

# ── AI Chat API ───────────────────────────────────────────────

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.get_json()
    message = data.get('message', '')
    lang = data.get('lang', 'en')

    # Basic rule-based replies (replace with real AI if needed)
    replies = {
        'en': f"You asked: '{message}'. Please check the Resources page for study materials.",
        'kn': f"ನೀವು ಕೇಳಿದ್ದು: '{message}'. ದಯವಿಟ್ಟು ಸಂಪನ್ಮೂಲಗಳ ಪುಟವನ್ನು ನೋಡಿ.",
        'hi': f"आपने पूछा: '{message}'. कृपया संसाधन पृष्ठ देखें।",
    }
    reply = replies.get(lang, replies['en'])
    return jsonify({'reply': reply})

# ── Performance Recommendation API ────────────────────────────

@app.route('/api/recommend', methods=['POST'])
def recommend():
    data = request.get_json()
    advice = []
    subject_names = {
        'kannada': 'Kannada',
        'english': 'English',
        'math': 'Math',
        'science': 'Science',
        'social': 'Social Science'
    }

    for subject, name in subject_names.items():
        score = int(data.get(subject, 0))
        if score < 35:
            advice.append(f"⚠️ {name}: You need urgent attention (score: {score}). Focus on basics.")
        elif score < 60:
            advice.append(f"📘 {name}: Needs improvement (score: {score}). Practice more questions.")
        elif score < 80:
            advice.append(f"👍 {name}: Good effort (score: {score}). Keep revising.")
        else:
            advice.append(f"🌟 {name}: Excellent (score: {score})! Keep it up.")

    return jsonify({'advice': advice})

# ── Run ───────────────────────────────────────────────────────

if __name__ == '__main__':
    app.run(debug=True)
