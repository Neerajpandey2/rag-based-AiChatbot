# app/routes/ask.py
from flask import Blueprint, request, jsonify
from flasgger import swag_from
from app.services.askGemini_service import GeminiService

ask_bp = Blueprint("ask", __name__)
gemini_service = GeminiService()

@ask_bp.route("/", methods=["POST"])
@swag_from({
    'tags': ['Gemini'],
    'summary': 'Ask Gemini',
    'description': 'Send a question to Gemini and get an AI-generated answer',
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'question': {
                        'type': 'string',
                        'example': 'What is AI?'
                    }
                },
                'required': ['question']
            }
        }
    ],
    'responses': {
        200: {
            'description': 'Gemini answer',
            'schema': {
                'type': 'object',
                'properties': {
                    'question': {'type': 'string'},
                    'answer': {'type': 'string'}
                }
            }
        },
        400: {
            'description': 'Missing question'
        },
        500: {
            'description': 'Gemini API error'
        }
    }
})
def ask():
    """
    Ask Gemini a question  
    ---
    post:
      tags:
        - Gemini
    """
    data = request.get_json() or {}
    question = data.get("question")

    if not question:
        return jsonify({"error": "No question provided"}), 400

    try:
        result = gemini_service.ask(question)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
