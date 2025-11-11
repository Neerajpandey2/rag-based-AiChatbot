# app/interfaces/pdf_interface.py
from abc import ABC, abstractmethod

class PDFInterface(ABC):
    @abstractmethod
    def process_pdf(self, file) -> dict:
        """Process PDF and return extracted Q&A pairs"""
        pass
