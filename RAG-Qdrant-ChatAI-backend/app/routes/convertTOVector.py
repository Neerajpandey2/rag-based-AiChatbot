# # app/routes/vectorize.py
# from flask import Blueprint, request, jsonify
# from flasgger import swag_from
# from app.services.llmGenerated_questionVectorization_service import VectorizeService

# vectorize_bp = Blueprint("vectorize", __name__)
# vectorize_service = VectorizeService()

# @vectorize_bp.route("/", methods=["POST"])
# @swag_from({
#     "tags": ["Vectorize"],
#     "summary": "Vectorize Q/A list",
#     "description": "Takes a list of question-answer pairs and returns vectors for each question.",
#     "parameters": [
#         {
#             "name": "body",
#             "in": "body",
#             "required": True,
#             "schema": {
#                 "type": "array",
#                 "items": {
#                     "type": "object",
#                     "properties": {
#                         "question": {"type": "string", "example": "What is AI?"},
#                         "answer": {"type": "string", "example": "AI is artificial intelligence."}
#                     },
#                     "required": ["question", "answer"]
#                 }
#             }
#         }
#     ],
#     "responses": {
#         200: {
#             "description": "List of Q/A with question vectors",
#             "examples": {
#                 "application/json": [
#                     {
#                         "question": "What is AI?",
#                         "answer": "AI is artificial intelligence.",
#                         "questionVector": [0.123, -0.456, 0.789]
#                     }
#                 ]
#             }
#         },
#         400: {"description": "Invalid input"},
#         500: {"description": "Internal server error"},
#     },
# })
# def vectorize():
#     """
#     Vectorize a list of question-answer pairs
#     """
#     data = request.get_json() or []

#     if not isinstance(data, list):
#         return jsonify({"error": "Payload must be a list of Q/A objects"}), 400

#     try:
#         enriched_data = vectorize_service.vectorize(data)
#         return jsonify(enriched_data)
#     except Exception as e:
#         return jsonify({"error": str(e)}), 500
