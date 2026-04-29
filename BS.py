from flask import Flask, render_template, request, jsonify
import json, os, re
from pathlib import Path
from dotenv import load_dotenv

# AI and Tool Imports
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.tools import tool
from langchain_community.tools import DuckDuckGoSearchRun

app = Flask(__name__)

# ── SETUP SECURITY & AI ──────────────────────────────────────────
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")

# Initialize the AI
llm = ChatOpenAI(model="gpt-4o-mini", temperature=0, openai_api_key=api_key)
search_tool = DuckDuckGoSearchRun()

@tool
def find_local_notes(topic: str):
    """Searches the computer for a folder matching the user's specific topic."""
    base_path = Path.cwd()
    for root, dirs, files in os.walk(base_path):
        for d in dirs:
            if topic.lower() in d.lower():
                return f"MATCH: Found your local folder for '{topic}' at: {os.path.join(root, d)}"
    return f"No local notes found for '{topic}' in the project directory."

tools = [search_tool, find_local_notes]
llm_with_tools = llm.bind_tools(tools)

# ── SUBJECT RESOURCES DATA ─────────────────────────────────────────
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
    {"name": "NSP – National Scholarship Portal", "url": "https://scholarships.gov.in/", "desc": "Central govt scholarships for students", "amount": "Up to ₹25,000/year"},
    {"name": "Karnataka Rajyotsava Scholarship", "url": "https://scholarships.gov.in/", "desc": "For Karnataka domicile students with merit", "amount": "₹5,000 – ₹15,000"},
    {"name": "PM YASASVI Scheme", "url": "https://yet.nta.ac.in/", "desc": "For OBC, EBC & DNT students", "amount": "₹75,000 – ₹1,25,000/year"},
]

# ── ROUTES ───────────────────────────────────────────────────────
@app.route('/')
@app.route('/index.html')
def index():
    return render_template('index.html')

@app.route('/resources.html')
def resources():
    return render_template('resources.html', resources=RESOURCES)

@app.route('/api/ai_chat', methods=['POST'])
def ai_chat():
    data = request.get_json()
    user_query = data.get("message", "")
    
    messages = [
        SystemMessage(content="You are a helpful Karnataka Board study assistant. Use find_local_notes for local files and duckduckgo_search for web links."),
        HumanMessage(content=user_query)
    ]
    
    try:
        ai_msg = llm_with_tools.invoke(messages)
        if ai_msg.tool_calls:
            messages.append(ai_msg)
            for tool_call in ai_msg.tool_calls:
                tool_map = {"duckduckgo_search": search_tool, "find_local_notes": find_local_notes}
                selected_tool = tool_map[tool_call["name"]]
                result = selected_tool.invoke(tool_call["args"])
                messages.append({"role": "tool", "tool_call_id": tool_call["id"], "content": str(result)})
            
            final_answer = llm_with_tools.invoke(messages)
            return jsonify({"reply": final_answer.content})
        
        return jsonify({"reply": ai_msg.content})
    except Exception as e:
        return jsonify({"reply": f"An error occurred: {str(e)}"}), 500

@app.route('/api/scholarships')
def scholarships():
    return jsonify(SCHOLARSHIPS)

if __name__ == '__main__':
    app.run(debug=True)
