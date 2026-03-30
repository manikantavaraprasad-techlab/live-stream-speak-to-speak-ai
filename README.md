# 🎙️ Speak-to-Speak AI Assistant

A real-time speech-to-speech AI assistant that converts voice input into intelligent responses using offline speech recognition and Large Language Models (LLMs).

---

## 🚀 Features

* 🎤 Speech-to-Text using Vosk (offline)
* 🧠 AI responses using Groq (LLaMA-based)
* 🔍 Entity detection using SQLite (FTS5)
* 🔊 Text-to-Speech using Edge-TTS
* ⚡ Real-time, low-latency processing

---

## 🛠️ Tech Stack

* Python
* Vosk
* Groq API
* SQLite (FTS5)
* Edge-TTS

---

## ▶️ How to Run

### 1. Clone Repository

```bash
git clone https://github.com/manikantavp-techlab/speak-to-speak-ai.git
cd speak-to-speak-ai
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Set Groq API Key

```bash
export GROQ_API_KEY="your_api_key"   # Linux/Mac
# set GROQ_API_KEY=your_api_key      # Windows
```

### 4. Download Vosk Model

Download from: https://alphacephei.com/vosk/models
Extract to:

```
~/vosk_models/vosk-model-small-en-us-0.15
```

### 5. Download Datasets

```bash
wget https://datasets.imdbws.com/name.basics.tsv.gz
wget https://datasets.imdbws.com/title.basics.tsv.gz
wget https://download.geonames.org/export/dump/allCountries.zip
unzip allCountries.zip
```

Move files:

```bash
mkdir -p entity_db/entity_db
mv name.basics.tsv.gz entity_db/entity_db/
mv title.basics.tsv.gz entity_db/entity_db/
mv allCountries.txt entity_db/entity_db/
```

### 6. Build Database

```bash
python build_db.py
```

### 7. Run Project

```bash
python main.py
```

---

## 💡 Example Queries

* "Who is Virat Kohli?"
* "Tell me about Elon Musk"
* "Where is Paris?"

---

## 🎥 Demo

*(Add your demo video link here)*

---

## 👨‍💻 Author

**Manikanta Vara Prasad**
