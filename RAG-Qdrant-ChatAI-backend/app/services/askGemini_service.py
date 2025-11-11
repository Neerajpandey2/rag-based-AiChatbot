# app/services/gemini_service.py
import requests
import os
from dotenv import load_dotenv
from app.interfaces.askGemini_interface import GeminiInterface

load_dotenv()

class GeminiService(GeminiInterface):
    def __init__(self):
        self.api_key = os.getenv("GEMINI_API_KEY")
        self.url =  os.getenv("GEMINI_URL")

    def ask(self, question: str) -> dict:
        headers = {
            "Content-Type": "application/json",
            "X-goog-api-key": self.api_key
        }
        payload = {"contents": [{"parts": [{"text": question}]}]}

        response = requests.post(self.url, headers=headers, json=payload, timeout=60)
        data = response.json()

        if response.status_code != 200:
            raise Exception(f"Gemini API error: {data}")

        answer_text = data["candidates"][0]["content"]["parts"][0]["text"]
        return {"question": question, "answer": answer_text}
