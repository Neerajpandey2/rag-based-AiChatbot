from flask import Blueprint, request, jsonify
from sentence_transformers import SentenceTransformer
from flasgger import swag_from
from app.services.qdrant_service import QdrantService

qdrant_bp = Blueprint('qdrant', __name__)
service = QdrantService()

@qdrant_bp.route("/create_collection", methods=["POST"])
@swag_from({
    'tags': ['Qdrant Collection'],
    'summary': 'Create a new collection',
    'description': 'Create a new collection for store questions and answers',
    'parameters': [
        {
            'name': 'text',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'name': {'type': 'string'}
                }
            }
        }
    ],
    'responses': {
        200: {
            'description': 'Embedding generated',
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
def create():
    data = request.get_json()
    name = data.get("name")
    if not name:
        return jsonify({"error": "Collection name required"}), 400
    return service.create_collection(name)

@qdrant_bp.route("/insert_Q&A", methods=["POST"])
@swag_from({
    'tags': ['Qdrant Collection'],
    'summary': 'Insert question and answers into a collection',
    'description': 'Inserts a question and answers with vector into the specified Qdrant collection.',
    'parameters': [
        {
            'name': 'collection_name',
            'in': 'query',
            'type': 'string',
            'required': True,
            'description': 'name'
        },
        {
            'name': 'question',
            'in': 'query',
            'type': 'string',
            'required': True,
            'description': 'Payload.Question'
        },
        {
            'name': 'answer',
            'in': 'query',
            'type': 'string',
            'required': True,
            'description': 'Payload.Answer'
        },
    ],
    'responses': {
        200: {
            'description': 'Data inserted successfully',
            'schema': {
                'type': 'object',
                'properties': {
                    'embedding': {
                        'success': {'type': 'boolean'},
                        'message': {'type': 'string'}
                    }
                }
            }
        }
    }
})
def insert():
    print("Request received for /insert_Q&A")
    data = request.get_json()
    collection = request.args.get('collection_name')
    question = data.get("question")
    answer = data.get("answer")  

    print("collection:", collection)
    print("question:", question)
    print("answer:", answer)

    try:
        if not service.does_collection_exist(collection):
            return jsonify({"error": f"Collection '{collection}' does not exist."}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500


    question_vector = request.args.getlist('vector', type=float)

    data = {
        "collection": collection,
        "question": question,
        "answer": answer,
        "question_vector": question_vector
    }

    print("insertion data : ",data)
    return service.insert_point(data)

@qdrant_bp.route("/search", methods=["POST"])
@swag_from({
    'tags': ['Qdrant Collection'],
    'summary': 'Search the questions and get top matched answer(s)',
    'description': 'Uses vector similarity to search a question and return the most relevant answer from the collection.',
    'parameters': [
        {
            'name': 'text',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'query': {'type': 'string'},
                    'collection': {'type': 'string'}
                }
            }
        }
    ],
    'responses': {
        200: {
            'description': 'Embedding generated',
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
def search():
    data = request.get_json()
    print(data)
    return service.search_point(data)



@qdrant_bp.route("/getQAsPaginated", methods=["GET"])
@swag_from({
    'tags': ['Qdrant Collection'],
    'summary': 'Get paginated questions and answers',
    'description': 'Fetches question-answer pairs from the specified Qdrant collection using pagination.',
    'parameters': [
        {
            'name': 'collection',
            'in': 'query',
            'type': 'string',
            'required': False,
            'default': 'CustomAi',
            'description': 'Name of the Qdrant collection'
        },
        {
            'name': 'limit',
            'in': 'query',
            'type': 'integer',
            'required': False,
            'default': 25,
            'description': 'Number of Q&A pairs to fetch per request'
        },
        {
            'name': 'offset',
            'in': 'query',
            'type': 'string',
            'required': False,
            'description': 'Scroll offset token returned from the previous call (for pagination)'
        }
    ],
    'responses': {
        200: {
            'description': 'Paginated list of questions and answers',
            'examples': {
                'application/json': {
                    "total_points": 240,
                    "fetched": 25,
                    "next_page_offset": "UUID-123",
                    "qa_list": [
                        {"id": "point-id-1", "question": "What is AI?", "answer": "Artificial Intelligence is..."}
                    ]
                }
            }
        },
        500: {
            'description': 'Internal server error'
        }
    }
})
def get_qa_paginated():
    collection = request.args.get("collection", "CustomAi")
    limit = int(request.args.get("limit", 25))
    offset = request.args.get("offset")  # may be None

    return service.get_questions_answers_paginated(collection_name=collection,limit=limit,offset=offset)


@qdrant_bp.route("/delete_collection", methods=["DELETE"])
@swag_from({
    'tags': ['Qdrant Collection'],
    'summary': 'Delete a Qdrant collection',
    'description': 'Deletes a Qdrant collection by name if it exists.',
    'parameters': [
        {
            'name': 'name',
            'in': 'query',
            'type': 'string',
            'required': True,
            'description': 'The name of the collection to delete'
        }
    ],
    'responses': {
        200: {
            'description': 'Collection deleted successfully',
            'examples': {
                'application/json': {
                    'message': "Collection 'my_collection' deleted successfully"
                }
            }
        },
        404: {
            'description': 'Collection not found',
            'examples': {
                'application/json': {
                    'error': "Collection 'my_collection' not found"
                }
            }
        },
        500: {
            'description': 'Internal server error',
            'examples': {
                'application/json': {
                    'error': "Something went wrong"
                }
            }
        }
    }
})
def delete():
    collection_name = request.args.get("name")
    if not collection_name:
        return jsonify({"error": "Collection name is required"}), 400
    return service.delete_collection(collection_name)


@swag_from({
    'tags': ['Qdrant Collection'],
    'summary': 'Get all questions and answers',
    'description': 'Fetches all stored question-answer pairs from the specified Qdrant collection.',
    'parameters': [
        {
            'name': 'collection',
            'in': 'query',
            'type': 'string',
            'required': False,
            'default': 'CustomAi',
            'description': 'Name of the Qdrant collection'
        }
    ],
    'responses': {
        200: {
            'description': 'List of questions and answers',
            'examples': {
                'application/json': [
                    {
                        "question": "What is AI?",
                        "answers": ["Artificial Intelligence is..."]
                    }
                ]
            }
        },
        500: {
            'description': 'Internal server error'
        }
    }
})
def get_all_qa():
    collection = request.args.get("collection", "CustomAi")
    return service.get_all_questions_answers(collection)

@qdrant_bp.route("/deleteQuestionById", methods=["DELETE"])
@swag_from({
    'tags': ['Qdrant Collection'],
    'summary': 'Delete a Qdrant question by ID',
    'description': 'Deletes a Qdrant question by Id.',
    'parameters': [
        {
            'name': 'collection_name',
            'in': 'query',
            'type': 'string',
            'required': False,
            'default': 'CustomAi',
            'description': 'Name of the Qdrant collection'
        },
        {
            'name': 'questionId',
            'in': 'query',
            'type': 'string',
            'required': True,
            'description': 'The id of the question to delete'
        }
    ],
    'responses': {
        200: {
            'description': 'Question deleted successfully',
            'examples': {
                'application/json': {
                    'message': "Question with id '123' deleted successfully"
                }
            }
        },
        404: {
            'description': 'Question not found',
            'examples': {
                'application/json': {
                    'error': "Question with id '123' not found"
                }
            }
        },
        500: {
            'description': 'Internal server error',
            'examples': {
                'application/json': {
                    'error': "Something went wrong"
                }
            }
        }
    }
})
def delete_question_by_id():
    collection_name = request.args.get("collection_name", "CustomAi")
    question_id = request.args.get("questionId")

    if not question_id:
        return jsonify({"error": "questionId is required"}), 400

    # just forward responsibility to service
    return service.delete_questionById(collection_name, question_id)


@qdrant_bp.route("/bulk_qa_insert", methods=["POST"])
@swag_from({
    'tags': ['Qdrant Collection'],
    'summary': 'Bulk insert Q&A items into a Qdrant collection',
    'description': 'Insert multiple questions and answers. Vectors will be automatically generated in the service before saving into Qdrant.',
    'parameters': [
        {
            'name': 'collection',
            'in': 'query',
            'type': 'string',
            'required': True,
            'description': 'The name of the Qdrant collection to insert data into'
        },
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'description': 'List of Q&A items (vectors auto-generated)',
            'schema': {
                'type': 'array',
                'items': {
                    'type': 'object',
                    'properties': {
                        'question': {'type': 'string', 'example': 'What is AI?'},
                        'answer': {'type': 'string', 'example': 'Artificial Intelligence is...'}
                    },
                    'required': ['question', 'answer']
                }
            }
        }
    ],
    'responses': {
        200: {
            'description': 'Bulk insert successful',
            'schema': {
                'type': 'object',
                'properties': {
                    'inserted_count': {'type': 'integer', 'example': 10},
                    'qdrant_response': {'type': 'object', 'example': {"status": {"completed": True}}}
                }
            }
        },
        400: {
            'description': 'Invalid request',
            'schema': {
                'type': 'object',
                'properties': {
                    'error': {'type': 'string', 'example': 'Collection name is required'}
                }
            }
        },
        500: {
            'description': 'Internal server error',
            'schema': {
                'type': 'object',
                'properties': {
                    'error': {'type': 'string', 'example': 'Something went wrong'}
                }
            }
        }
    }
})
def bulk_insert():
    collection_name = request.args.get("collection")
    if not collection_name:
        return jsonify({"error": "Collection name is required"}), 400

    data = request.get_json()
    if not data or not isinstance(data, list):
        return jsonify({"error": "A list of QA items is required"}), 400

    try:
        return service.bulk_qa_insert(data, collection_name)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    

@qdrant_bp.route("/update_QA", methods=["PUT"])
@swag_from({
    'tags': ['Qdrant Collection'],
    'summary': 'Update a Q&A item by ID',
    'description': 'Overwrites an existing Q&A point with new question, answer, and regenerated vector.',
    'parameters': [
        {
            'name': 'collection_name',
            'in': 'query',
            'type': 'string',
            'required': True,
            'description': 'The name of the Qdrant collection'
        },
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'schema': {
                'type': 'object',
                'properties': {
                    'id': {'type': 'string', 'example': '123'},   # better to keep string, Qdrant IDs are strings
                    'question': {'type': 'string', 'example': 'What is AI?'},
                    'answer': {'type': 'string', 'example': 'Artificial Intelligence is...'}
                },
                'required': ['id', 'question', 'answer']
            }
        }
    ],
    'consumes': [
        'application/json'   # this is important, tells Swagger UI what content-type to send
    ],
    'responses': {
        200: {
            'description': 'Q&A updated successfully',
            'schema': {
                'type': 'object',
                'properties': {
                    'success': {'type': 'boolean'},
                    'message': {'type': 'string'}
                }
            }
        },
        400: {
            'description': 'Invalid request',
            'schema': {
                'type': 'object',
                'properties': {
                    'error': {'type': 'string'}
                }
            }
        },
        500: {
            'description': 'Internal server error',
            'schema': {
                'type': 'object',
                'properties': {
                    'error': {'type': 'string'}
                }
            }
        }
    }
})
def update_qa():
    collection = request.args.get("collection_name")
    if not collection:
        return jsonify({"error": "Collection name is required"}), 400

    data = request.get_json()
    if not data:
        return jsonify({"error": "Request body is required"}), 400

    point_id = data.get("id")
    question = data.get("question")
    answer = data.get("answer")

    if not point_id or not question or not answer:
        return jsonify({"error": "id, question, and answer are required"}), 400

    try:
        # Delegate update to service
        print("process start")
        return service.update_point(collection, point_id, question, answer)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@qdrant_bp.route("/total_QA", methods=["GET"])
@swag_from({
    'tags': ['Qdrant Collection'],
    'summary': 'Get total QA count in a collection',
    'description': 'Returns the total number of Q&A entries stored in the specified Qdrant collection.',
    'parameters': [
        {
            'name': 'collection',
            'in': 'query',
            'type': 'string',
            'required': True,
            'description': 'The name of the Qdrant collection'
        }
    ],
    'responses': {
        200: {
            'description': 'Total QA count',
            'examples': {
                'application/json': {
                    "collection": "CustomAi",
                    "total_QA": 1523
                }
            }
        },
        400: {
            'description': 'Invalid request',
            'examples': {
                'application/json': {
                    "error": "Collection name is required"
                }
            }
        },
        500: {
            'description': 'Internal server error'
        }
    }
})
def get_total_qa():
    collection = request.args.get("collection")
    if not collection:
        return jsonify({"error": "Collection name is required"}), 400
    try:
        total_count = service.get_total_qa(collection)
        return jsonify({"collection": collection, "total_QA": total_count})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


