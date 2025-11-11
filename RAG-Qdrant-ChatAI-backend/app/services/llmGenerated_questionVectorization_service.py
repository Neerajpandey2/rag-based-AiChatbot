# # app/services/vectorize_service.py
# from typing import List, Dict, Any
# from sentence_transformers import SentenceTransformer
# from app.interfaces.llmGenerated_questionVectorization_interface import VectorizeInterface

# class VectorizeService(VectorizeInterface):
#     def __init__(self):
#         # Load once at startup
#         self.embedding_model = SentenceTransformer("sentence-transformers/all-mpnet-base-v2")

#     def vectorize(self, qa_list: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
#         questions = [item.get("question") for item in qa_list]
#         vectors = self.embedding_model.encode(questions).tolist()

#         enriched = []
#         for item, vec in zip(qa_list, vectors):
#             enriched.append({
#                 "question": item.get("question"),
#                 "answers": item.get("answer"),
#                 "vector": vec
#             })
#         return enriched
