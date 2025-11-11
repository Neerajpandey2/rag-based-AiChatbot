# app/interfaces/gemini_interface.py
from abc import ABC, abstractmethod

class GeminiInterface(ABC):
    @abstractmethod
    def ask(self, question: str) -> dict:
        """Send a question and return {'question': q, 'answer': a}"""
        pass
