from flask import Flask, render_template, request, jsonify
import json, os, re

app = Flask(__name__)

SUBJECTS = ["kannada", "hindi", "sanskrit", "english", "maths", "science", "social_science"]

RESOURCES = {
    "kannada": {
        "name": "ಕನ್ನಡ (Kannada)",
        "icon": "📖",
        "color": "#e8a020",
        "textbooks": [
            {"title": "Class 8 Kannada Textbook – KSEEB", "url": "https://ktbs.kar.nic.in/new/website%20books/class8/8th-kan-kannada1.pdf"},
            {"title": "Class 9 Kannada Textbook – KSEEB", "url": "https://ktbs.kar.nic.in/new/website%20books/class9/9th-kan-kannada1.pdf"},
            {"title": "Class 10 Kannada Textbook – KSEEB", "url": "https://ktbs.kar.nic.in/new/website%20books/class10/10th-kan-kannada1.pdf"},
        ],
        "question_papers": [
            {"title": "SSLC Kannada Previous Year Paper 2023", "url": "https://www.kseeb.kar.nic.in/"},
            {"title": "SSLC Kannada Model Paper 2024", "url": "https://www.kseeb.kar.nic.in/"},
            {"title": "Kannada Practice Paper Set", "url": "https://www.kseeb.kar.nic.in/"},
        ],
        "topics": ["ಗದ್ಯ (Prose)", "ಪದ್ಯ (Poetry)", "ವ್ಯಾಕರಣ (Grammar)", "ಪತ್ರ ಲೇಖನ (Letter Writing)", "ಪ್ರಬಂಧ (Essay)"]
    },
    "hindi": {
        "name": "हिंदी (Hindi)",
        "icon": "📝",
        "color": "#e85d04",
        "textbooks": [
            {"title": "Class 8 Hindi – NCERT Vasant", "url": "https://ncert.nic.in/textbook.php?fhvs1=0-9"},
            {"title": "Class 9 Hindi – NCERT Kshitij", "url": "https://ncert.nic.in/textbook.php?ihhk1=0-17"},
            {"title": "Class 10 Hindi – NCERT Kshitij 2", "url": "https://ncert.nic.in/textbook.php?jhhk1=0-16"},
        ],
        "question_papers": [
            {"title": "CBSE Class 10 Hindi Paper 2023", "url": "https://cbseacademic.nic.in/"},
            {"title": "Hindi Sample Paper 2024", "url": "https://cbseacademic.nic.in/"},
            {"title": "KSEEB Hindi Model Paper", "url": "https://www.kseeb.kar.nic.in/"},
        ],
        "topics": ["गद्य (Prose)", "पद्य (Poetry)", "व्याकरण (Grammar)", "लेखन (Writing)", "अपठित (Unseen)"]
    },
    "sanskrit": {
        "name": "संस्कृत (Sanskrit)",
        "icon": "🕉️",
        "color": "#7b2d8b",
        "textbooks": [
            {"title": "Class 8 Sanskrit – NCERT Ruchira", "url": "https://ncert.nic.in/textbook.php?hsrt1=0-15"},
            {"title": "Class 9 Sanskrit – NCERT Shemushi", "url": "https://ncert.nic.in/textbook.php?isrt1=0-15"},
            {"title": "Class 10 Sanskrit – NCERT Shemushi 2", "url": "https://ncert.nic.in/textbook.php?jsrt1=0-15"},
        ],
        "question_papers": [
            {"title": "CBSE Sanskrit Sample Paper 2024", "url": "https://cbseacademic.nic.in/"},
            {"title": "KSEEB Sanskrit Previous Paper", "url": "https://www.kseeb.kar.nic.in/"},
            {"title": "Sanskrit Practice Set", "url": "https://ncert.nic.in/"},
        ],
        "topics": ["गद्यांश (Prose)", "पद्यांश (Poetry)", "व्याकरण (Grammar)", "अनुवाद (Translation)", "रचना (Composition)"]
    },
    "english": {
        "name": "English",
        "icon": "🔤",
        "color": "#0077b6",
        "textbooks": [
            {"title": "Class 8 English – NCERT Honeydew", "url": "https://ncert.nic.in/textbook.php?fehl1=0-10"},
            {"title": "Class 9 English – NCERT Beehive", "url": "https://ncert.nic.in/textbook.php?iehl1=0-11"},
            {"title": "Class 10 English – NCERT First Flight", "url": "https://ncert.nic.in/textbook.php?jehl1=0-11"},
        ],
        "question_papers": [
            {"title": "CBSE Class 10 English Paper 2023", "url": "https://cbseacademic.nic.in/"},
            {"title": "English Sample Paper 2024", "url": "https://cbseacademic.nic.in/"},
            {"title": "KSEEB English Previous Papers", "url": "https://www.kseeb.kar.nic.in/"},
        ],
        "topics": ["Reading Comprehension", "Grammar & Writing", "Literature", "Vocabulary", "Letter/Essay Writing"]
    },
    "maths": {
        "name": "ಗಣಿತ (Maths)",
        "icon": "🔢",
        "color": "#2d6a4f",
        "textbooks": [
            {"title": "Class 8 Maths – NCERT", "url": "https://ncert.nic.in/textbook.php?fmth1=0-16"},
            {"title": "Class 9 Maths – NCERT", "url": "https://ncert.nic.in/textbook.php?imth1=0-15"},
            {"title": "Class 10 Maths – NCERT", "url": "https://ncert.nic.in/textbook.php?jmth1=0-15"},
        ],
        "question_papers": [
            {"title": "CBSE Class 10 Maths Standard 2023", "url": "https://cbseacademic.nic.in/"},
            {"title": "Maths Sample Paper 2024", "url": "https://cbseacademic.nic.in/"},
            {"title": "KSEEB Maths Previous Papers", "url": "https://www.kseeb.kar.nic.in/"},
        ],
        "topics": ["Algebra", "Geometry", "Trigonometry", "Statistics", "Number Systems", "Arithmetic"]
    },
    "science": {
        "name": "ವಿಜ್ಞಾನ (Science)",
        "icon": "🔬",
        "color": "#1d7874",
        "textbooks": [
            {"title": "Class 8 Science – NCERT", "url": "https://ncert.nic.in/textbook.php?hesc1=0-18"},
            {"title": "Class 9 Science – NCERT", "url": "https://ncert.nic.in/textbook.php?iesc1=0-15"},
            {"title": "Class 10 Science – NCERT", "url": "https://ncert.nic.in/textbook.php?jesc1=0-16"},
        ],
        "question_papers": [
            {"title": "CBSE Class 10 Science Paper 2023", "url": "https://cbseacademic.nic.in/"},
            {"title": "Science Sample Paper 2024", "url": "https://cbseacademic.nic.in/"},
            {"title": "KSEEB Science Previous Papers", "url": "https://www.kseeb.kar.nic.in/"},
        ],
        "topics": ["Physics", "Chemistry", "Biology", "Environmental Science", "Natural Phenomena"]
    },
    "social_science": {
        "name": "ಸಮಾಜ ವಿಜ್ಞಾನ (Social Science)",
        "icon": "🌍",
        "color": "#6b4226",
        "textbooks": [
            {"title": "Class 8 Social Science – NCERT", "url": "https://ncert.nic.in/textbook.php?hess1=0-10"},
            {"title": "Class 9 Social Science – NCERT", "url": "https://ncert.nic.in/textbook.php?iess1=0-6"},
            {"title": "Class 10 Social Science – NCERT", "url": "https://ncert.nic.in/textbook.php?jess1=0-5"},
        ],
        "question_papers": [
            {"title": "CBSE Social Science Paper 2023", "url": "https://cbseacademic.nic.in/"},
            {"title": "Social Science Sample Paper 2024", "url": "https://cbseacademic.nic.in/"},
            {"title": "KSEEB Social Science Papers", "url": "https://www.kseeb.kar.nic.in/"},
        ],
        "topics": ["History", "Geography", "Civics/Political Science", "Economics", "Disaster Management"]
    }
}

SCHOLARSHIPS = [
    {"name": "NSP – National Scholarship Portal", "url": "https://scholarships.gov.in/", "desc": "Central govt scholarships for SC/ST/OBC/Minority/EWS students", "amount": "Up to ₹25,000/year"},
    {"name": "Karnataka Rajyotsava Scholarship", "url": "https://scholarships.gov.in/", "desc": "For Karnataka domicile students with merit", "amount": "₹5,000 – ₹15,000"},
    {"name": "PM YASASVI Scheme", "url": "https://yet.nta.ac.in/", "desc": "For OBC, EBC & DNT students in Class 9 & 11", "amount": "₹75,000 – ₹1,25,000/year"},
    {"name": "Mukhyamantri Medhavi Vidyarthi Yojana", "url": "https://mmvy.mp.gov.in/", "desc": "Merit-based scholarship for rural students", "amount": "Full tuition fee"},
    {"name": "Prerana Scholarship – Karnataka", "url": "https://ssp.postmatric.karnataka.gov.in/", "desc": "Post-matric scholarship for SC/ST students in Karnataka", "amount": "Up to ₹12,000/year"},
]

def get_recommendation(subject, marks):
    if marks >= 85:
        level = "advanced"
        msg = "Excellent! You're performing brilliantly. Focus on challenging problems and olympiad preparation."
        tasks = ["Solve HOTS (Higher Order Thinking) questions", "Attempt previous year board papers", "Explore advanced topics beyond syllabus", "Mentor peers to strengthen your own understanding"]
        color = "#2d6a4f"
        emoji = "🌟"
    elif marks >= 65:
        level = "intermediate"
        msg = "Good work! A little more practice and you'll master this subject."
        tasks = ["Revise weak chapters identified in tests", "Practice 15 questions daily", "Make summary notes for revision", "Take chapter-wise mock tests"]
        color = "#e8a020"
        emoji = "📈"
    elif marks >= 40:
        level = "basic"
        msg = "You're on the right track. Let's build a strong foundation together."
        tasks = ["Re-read NCERT chapters carefully", "Watch video explanations for concepts", "Solve 5 basic problems daily", "Ask your teacher for extra help on weak topics"]
        color = "#e85d04"
        emoji = "💪"
    else:
        level = "foundation"
        msg = "Don't worry! With consistent effort you can improve greatly. Start from basics."
        tasks = ["Start from Chapter 1 – read slowly and take notes", "Watch simple YouTube explanations", "Practice 3 basic problems every day", "Talk to your teacher about a study plan"]
        color = "#c1121f"
        emoji = "🌱"
    return {"level": level, "message": msg, "tasks": tasks, "color": color, "emoji": emoji}

@app.route("/")
def index():
    return render_template("index.html", resources=RESOURCES, scholarships=SCHOLARSHIPS)

@app.route("/api/resources/<subject>")
def get_resources(subject):
    if subject in RESOURCES:
        return jsonify(RESOURCES[subject])
    return jsonify({"error": "Subject not found"}), 404

@app.route("/api/recommendation", methods=["POST"])
def recommendation():
    data = request.json
    results = {}
    for subject, marks in data.get("marks", {}).items():
        results[subject] = get_recommendation(subject, int(marks))
    return jsonify(results)

@app.route("/api/scholarships")
def scholarships():
    return jsonify(SCHOLARSHIPS)

@app.route("/api/chat", methods=["POST"])
def chat():
    msg = request.json.get("message", "").lower().strip()
    lang = request.json.get("lang", "en")
    
    responses_en = {
        "scholarship": "Great question! Here are scholarships for you:\n• NSP (scholarships.gov.in) – for SC/ST/OBC/Minority\n• PM YASASVI – for OBC/EBC students\n• Karnataka Rajyotsava Scholarship\n\nVisit the Scholarships tab for details! 🎓",
        "study": "Here's a good study plan:\n✅ Study 4-5 hours daily\n✅ Take 10-min breaks every hour\n✅ Revise previous topics on weekends\n✅ Use NCERT textbooks as your base\n✅ Practice past papers monthly",
        "career": "Career paths after 10th:\n🔬 Science stream → Doctor, Engineer, Researcher\n💼 Commerce → CA, Banking, Business\n📚 Arts → Teacher, Lawyer, Journalist, Civil Services\n\nChoose based on your interest and strengths!",
        "maths": "For Maths improvement:\n📐 Practice daily – even 10 problems help\n📖 Master NCERT examples first\n🧮 Learn formulas by writing them\n✏️ Show full working in exams",
        "science": "For Science:\n🔬 Understand concepts – don't just memorize\n📝 Draw diagrams for Biology\n⚗️ Learn chemical equations\n🌡️ Connect Physics to real life",
        "english": "For English:\n📰 Read newspaper headlines daily\n✍️ Write a short paragraph every day\n🗣️ Speak English for 10 min daily\n📖 Read NCERT lessons carefully",
        "hello": "Hello! I'm EduBot, your learning assistant. Ask me about:\n• Scholarships 🎓\n• Study tips 📚\n• Career guidance 💼\n• Subject help 🔬",
        "help": "I can help you with:\n📚 Study tips and plans\n🎓 Scholarship information\n💼 Career guidance\n🔬 Subject-specific advice\n\nWhat would you like to know?",
        "default": "That's a great question! I'm here to help with studies, scholarships, and career guidance. Could you be more specific? For example:\n• 'How to improve in Maths?'\n• 'Which scholarships are available?'\n• 'What career after 10th?'"
    }
    
    responses_kn = {
        "scholarship": "ವಿದ್ಯಾರ್ಥಿ ವೇತನಗಳು:\n• NSP (scholarships.gov.in) – SC/ST/OBC ವಿದ್ಯಾರ್ಥಿಗಳಿಗೆ\n• PM YASASVI – OBC ವಿದ್ಯಾರ್ಥಿಗಳಿಗೆ\n• ಕರ್ನಾಟಕ ರಾಜ್ಯೋತ್ಸವ ಶಿಷ್ಯವೇತನ\n\nಹೆಚ್ಚಿನ ಮಾಹಿತಿಗಾಗಿ Scholarships ಟ್ಯಾಬ್ ನೋಡಿ! 🎓",
        "study": "ಅಧ್ಯಯನ ಯೋಜನೆ:\n✅ ದಿನಕ್ಕೆ 4-5 ಗಂಟೆ ಓದಿ\n✅ ಪ್ರತಿ ಗಂಟೆಗೆ 10 ನಿಮಿಷ ವಿಶ್ರಾಂತಿ\n✅ ವಾರಾಂತ್ಯದಲ್ಲಿ ಪರಿಶೀಲಿಸಿ\n✅ NCERT ಪಠ್ಯಪುಸ್ತಕಗಳನ್ನು ಬಳಸಿ",
        "hello": "ನಮಸ್ಕಾರ! ನಾನು EduBot. ನಿಮಗೆ ಇವುಗಳ ಬಗ್ಗೆ ಸಹಾಯ ಮಾಡಬಲ್ಲೆ:\n• ವಿದ್ಯಾರ್ಥಿ ವೇತನ 🎓\n• ಅಧ್ಯಯನ ಸಲಹೆ 📚\n• ವೃತ್ತಿ ಮಾರ್ಗದರ್ಶನ 💼",
        "default": "ನಿಮ್ಮ ಪ್ರಶ್ನೆ ಸ್ಪಷ್ಟಪಡಿಸಿ. ಉದಾಹರಣೆಗೆ:\n• 'ಗಣಿತದಲ್ಲಿ ಹೇಗೆ ಸುಧಾರಿಸಬಹುದು?'\n• 'ಯಾವ ವಿದ್ಯಾರ್ಥಿ ವೇತನ ಲಭ್ಯ?'"
    }
    
    responses = responses_kn if lang == "kn" else responses_en
    
    reply = responses["default"]
    for key in responses:
        if key in msg:
            reply = responses[key]
            break
    
    return jsonify({"reply": reply})

if __name__ == "__main__":
    app.run(debug=True, port=5000)
