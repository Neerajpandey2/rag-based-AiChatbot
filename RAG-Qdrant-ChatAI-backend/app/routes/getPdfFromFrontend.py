# app/routes/upload.py
from flask import Blueprint, request, jsonify
from flasgger import swag_from
from app.services.pdf_service import PDFService

upload_bp = Blueprint("upload", __name__)
pdf_service = PDFService()

@upload_bp.route("/", methods=["POST"])
@swag_from({
    'tags': ['PDF'],
    'summary': 'Upload PDF and extract Q&A',
    'description': 'Upload a PDF file, extract Q&A pairs (no vectorization, no Qdrant insertion)',
    'consumes': ['multipart/form-data'],
    'parameters': [
        {
            'name': 'file',
            'in': 'formData',
            'type': 'file',
            'required': True,
            'description': 'The PDF file to upload'
        }
    ],
    'responses': {
        200: {
            'description': 'Processing complete, Q&A extracted',
            'schema': {
                'type': 'object',
                'properties': {
                    'message': {'type': 'string', 'example': 'Processing complete'},
                    'qa_pairs': {
                        'type': 'array',
                        'items': {
                            'type': 'object',
                            'properties': {
                                'question': {'type': 'string'},
                                'answers': {'type': 'array', 'items': {'type': 'string'}}
                            }
                        }
                    },
                    'total_chunks': {'type': 'integer'},
                    'total_qa_generated': {'type': 'integer'}
                }
            }
        },
        400: {
            'description': 'Invalid request (e.g. no file provided or PDF parsing failed)'
        }
    }
})
def upload_pdf():
    """
    Upload a PDF, extract Q&A (without vectorization or Qdrant insert)
    """
    if "file" not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files["file"]
    print("file received:", file.filename)

    try:
        final_output = pdf_service.process_pdf(file)

        return jsonify({
            "message": "Processing complete",
            "qa_pairs": final_output["qa_results"],
            "total_chunks": final_output["total_chunks"],
            "total_qa_generated": final_output["total_qa_generated"]
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 400
