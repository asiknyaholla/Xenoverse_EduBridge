## Readme
# 🎓 EduBridge – Smart Learning Access Platform for Rural Students

## 🌟 Overview
**EduBridge** is a lightweight web platform built using Python and Flask to help rural students access quality education in a simple, accessible, and low-bandwidth way.

It solves key challenges:
- Lack of learning resources  
- No personalized guidance  
- Language barriers  
- Limited awareness of study strategies  

---

## 🚀 Features

### 🤖 AI Study Assistant (Chatbot)
- Answers student queries
- Gives subject-wise study tips
- Works offline (low bandwidth)

### 🌐 Language Toggle
Supports:
- English  
- Kannada  
- Hindi  

### 📊 Personalized Learning Plan
- Input subject-wise marks  
- Detects weak & strong subjects  
- Suggests improvement strategy  

### 📈 Performance Graph
- Visualize marks using charts (Chart.js)

### 🔊 Text-to-Speech
- Converts chatbot replies into speech  
- Helps students with reading difficulty  

### 📚 Subject Resources
Includes:
- Kannada  
- Hindi  
- Sanskrit  
- English  
- Mathematics  
- Science  
- Social Science  

---

## 🧠 Tech Stack

- Backend: Python (Flask)  
- Frontend: HTML, CSS, JavaScript  
- Charts: Chart.js  
- Speech: Web Speech API  

---

## 📁 Project Structure
edubridge/
│── app.py
│
├── services/
│ ├── init.py
│ ├── chatbot.py
│ ├── recommender.py
│ ├── translator.py
│
├── templates/
│ ├── index.html
│ ├── resources.html
│
├── static/
│ ├── styles.css
│ ├── app.js

## ⚙️ Setup Instructions

### 1. Clone Repository

git clone https://github.com/your-username/edubridge.git

cd edubridge


### 2. Create Virtual Environment

python -m venv venv
venv\Scripts\activate


### 3. Install Dependencies

pip install flask


### 4. Run Application

python app.py


### 5. Open Browser

http://127.0.0.1:5000


---

## 📶 Low Bandwidth Optimization
- Minimal UI design  
- No heavy images  
- Offline chatbot logic  
- Browser-based text-to-speech  

---

## 🎯 Target Users
- Rural students (SSLC / Class 10)
- Students with limited internet access
- Learners needing simple explanations

---

## 🏆 Hackathon Highlights

### 💡 Innovation
- Combines chatbot + learning + analytics  
- Works in low-resource environments  

### 🌍 Social Impact
- Bridges rural education gap  
- Promotes inclusive learning  

### ⚡ Scalability
- Can expand to:
  - AI tutor
  - Scholarships
  - Student accounts  

---

## 🔮 Future Scope
- 🎙 Speech-to-text input  
- 📱 Mobile app  
- 🧑‍🎓 Student dashboards  
- 🌐 Full multilingual support  
- 🤖 Advanced AI chatbot  

---

## 👨‍💻 Developed For
Hackathon Project – Education + Accessibility + AI

---

## 📜 License
For educational and hackathon use only.

---

## ✨ Tagline
**Empowering Rural Students with Smart Learning**
