let currentLang = "en";

// Chat
function sendMessage() {
    let msg = document.getElementById("input").value;

    fetch('/api/chat', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({
            message: msg,
            lang: currentLang
        })
    })
    .then(res => res.json())
    .then(data => {
        document.getElementById("reply").innerText = data.reply;
        speak(data.reply);
    });
}

// Language toggle
function setLanguage(lang) {
    currentLang = lang;
    alert("Language switched");
}

// TTS (Better than pyttsx3 → no lag)
function speak(text) {
    let speech = new SpeechSynthesisUtterance(text);
    speech.lang = currentLang === "kn" ? "kn-IN" :
                  currentLang === "hi" ? "hi-IN" : "en-US";
    window.speechSynthesis.speak(speech);
}

// Recommendation
function getPlan() {
    let subjects = ["math", "science", "english"];
    let data = {};

    subjects.forEach(sub => {
        data[sub] = document.getElementById(sub).value;
    });

    fetch('/api/recommend', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify(data)
    })
    .then(res => res.json())
    .then(res => {
        document.getElementById("plan").innerText = res.advice.join(", ");
        drawChart(data);
    });
}

// Graph
function drawChart(data){
    new Chart(document.getElementById("chart"), {
        type: 'bar',
        data: {
            labels: Object.keys(data),
            datasets: [{
                data: Object.values(data)
            }]
        }
    });
}