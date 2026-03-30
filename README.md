# 🎙️ Speak-to-Speak AI Assistant

A real-time speech-to-speech AI assistant that converts voice input into intelligent responses using offline speech recognition and LLM.

---

## 🚀 Features

* 🎤 Speech-to-Text (Vosk)
* 🧠 AI Responses (Groq LLM)
* 🔍 Entity Detection (SQLite)
* 🔊 Text-to-Speech (Edge-TTS)
* ⚡ Real-time processing

---

## 🛠️ Tech Stack

* Python
* Vosk
* Groq API
* SQLite
* Edge-TTS

---

## ▶️ How to Run

```bash
# 1. Clone repository
git clone https://github.com/manikantavp-techlab/speak-to-speak-ai.git
cd speak-to-speak-ai

# 2. Install dependencies
pip install -r requirements.txt

# 3. Set Groq API Key
export GROQ_API_KEY="your_api_key"   # Linux/Mac
# set GROQ_API_KEY=your_api_key      # Windows

# 4. Download Vosk Model
# Download from: https://alphacephei.com/vosk/models
# Extract to: ~/vosk_models/vosk-model-small-en-us-0.15

# 5. Download Datasets
wget https://datasets.imdbws.com/name.basics.tsv.gz
wget https://datasets.imdbws.com/title.basics.tsv.gz
wget https://download.geonames.org/export/dump/allCountries.zip
unzip allCountries.zip

# Move files into correct structure:
mkdir -p entity_db/entity_db
mv name.basics.tsv.gz entity_db/entity_db/
mv title.basics.tsv.gz entity_db/entity_db/
mv allCountries.txt entity_db/entity_db/

# 6. Build Database
python build_db.py

# 7. Run Project
python main.py
```

---

## 💡 Example Queries

* "Who is Virat Kohli?"
* "Tell me about Elon Musk"

---

## 🎥 Demo

(Loading......)

---

## 👨‍💻 Author

Manikanta Vara Prasad
