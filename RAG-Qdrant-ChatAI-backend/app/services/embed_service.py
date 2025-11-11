from sentence_transformers import SentenceTransformer
from app.interfaces.embed_interface import EmbedInterface

class EmbedService(EmbedInterface):
    def __init__(self):
        # Using all-mpnet-base-v2 for balanced performance + accuracy
        self.model = SentenceTransformer("sentence-transformers/all-mpnet-base-v2")

    def get_embedding(self, text: str):
        # Normalize embeddings for better semantic search consistency
        return self.model.encode(text, normalize_embeddings=True).tolist()
