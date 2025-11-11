from abc import ABC, abstractmethod
from typing import List

class EmbedInterface(ABC):
    @abstractmethod
    def get_embedding(self, text: str) -> List[float]:
        """Generate an embedding for the given text"""
        pass
