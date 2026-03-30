#!/usr/bin/env python3
import os
import json
import time
import queue
import asyncio
import sqlite3
from dataclasses import dataclass

import numpy as np
import sounddevice as sd
import soundfile as sf
from vosk import Model, KaldiRecognizer
from groq import Groq
import edge_tts


@dataclass
class Config:
    vosk_model_path: str = os.path.expanduser("~/vosk_models/vosk-model-small-en-us-0.15")
    sample_rate: int = 16000
    blocksize: int = 1600

    groq_model: str = "llama-3.3-70b-versatile"
    max_tokens: int = 150
    temperature: float = 0.5

    tts_voice: str = "en-US-JennyNeural"
    tts_out_wav: str = "reply.wav"

    db_path: str = "knowledge.db"


class SpeakToSpeak:
    def __init__(self, cfg: Config):
        self.cfg = cfg

        api_key = os.environ.get("GROQ_API_KEY")
        if not api_key:
            raise RuntimeError("Set GROQ_API_KEY")

        if not os.path.isdir(cfg.vosk_model_path):
            raise RuntimeError("Vosk model not found")

        self.client = Groq(api_key=api_key)
        self.model = Model(cfg.vosk_model_path)
        self.rec = KaldiRecognizer(self.model, cfg.sample_rate)

        self.audio_q = queue.Queue()
        self.utt_buf = bytearray()

    # 🔍 Entity Detection (SQLite FTS)
    def detect_entities(self, text):
        try:
            con = sqlite3.connect(self.cfg.db_path)
            cur = con.cursor()
            words = text.split()

            found = []
            for w in words:
                cur.execute("SELECT name FROM entities WHERE name MATCH ? LIMIT 1", (w,))
                r = cur.fetchone()
                if r:
                    found.append(r[0])

            con.close()
            return list(set(found))
        except:
            return []

    def audio_callback(self, indata, frames, time_info, status):
        self.audio_q.put(bytes(indata))

    def start_mic(self):
        self.stream = sd.RawInputStream(
            samplerate=self.cfg.sample_rate,
            blocksize=self.cfg.blocksize,
            dtype="int16",
            channels=1,
            callback=self.audio_callback,
        )
        self.stream.start()

    def ask_groq(self, text):
        resp = self.client.chat.completions.create(
            model=self.cfg.groq_model,
            messages=[
                {"role": "system", "content": "Answer in 1-2 short sentences."},
                {"role": "user", "content": text},
            ],
            max_tokens=self.cfg.max_tokens,
            temperature=self.cfg.temperature,
        )
        return resp.choices[0].message.content.strip()

    async def tts(self, text):
        await edge_tts.Communicate(text=text, voice=self.cfg.tts_voice).save(self.cfg.tts_out_wav)

    def speak(self, text):
        asyncio.run(self.tts(text))
        data, sr = sf.read(self.cfg.tts_out_wav)
        sd.play(data, sr)
        sd.wait()

    def run(self):
        print("🎙️ Speak-to-Speak AI Started...")
        self.start_mic()

        while True:
            data = self.audio_q.get()
            self.utt_buf.extend(data)

            if self.rec.AcceptWaveform(data):
                res = json.loads(self.rec.Result())
                text = res.get("text", "").strip()

                if not text:
                    continue

                print(f"👤 You: {text}")

                # 🔥 Entity boost
                entities = self.detect_entities(text)
                if entities:
                    text += " Context: " + ", ".join(entities)

                try:
                    reply = self.ask_groq(text)
                except Exception as e:
                    reply = "Error connecting to AI."

                print(f"🤖 Bot: {reply}")
                self.speak(reply)

                self.utt_buf.clear()


if __name__ == "__main__":
    cfg = Config()
    SpeakToSpeak(cfg).run()
