from flask import Blueprint, request, jsonify
from flasgger import swag_from
from app.services.embed_service import EmbedService

api_bp = Blueprint('api', __name__)
embed_service = EmbedService()

@api_bp.route('/vectorEmbed', methods=['POST'])
@swag_from({
    'tags': ['Vector Transformation'],
    'summary': 'Change into vector format',
    'description': 'Convert text format into vector format',
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'text': {'type': 'string'}
                },
                'required': ['text']
            }
        }
    ],
    'responses': {
        200: {
            'description': 'Returns sentence embedding',
            'schema': {
                'type': 'object',
                'properties': {
                    'embedding': {
                        'type': 'array',
                        'items': {'type': 'number'}
                    }
                }
            }
        }
    }
})
def embed():
    data = request.get_json()
    if not data or "text" not in data:
        return jsonify({"error": "Text field is required"}), 400
    try:
        embedding = embed_service.get_embedding(data["text"].strip())
        return jsonify({"embedding": embedding})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
