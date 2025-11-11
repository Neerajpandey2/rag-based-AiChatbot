from typing import Dict, Any ,List
import requests
import uuid
import json
from flask import Response
from flask import jsonify
from app.services.embed_service import EmbedService
from config import QDRANT_HOST
from app.interfaces.qdrant_interface import QdrantInterface
from logger import log_line
from helpers.get_humanLike_answer_helper import get_human_like_answer
from app.services.askGemini_service import GeminiService
from helpers.pdf_helper import vectorize_qa_list
import traceback
import math

embed_service = EmbedService()

class QdrantService(QdrantInterface):

    def __init__(self):
        self.gemini_service = GeminiService()

    def create_collection(self, name: str):
        payload = {
            "vectors": {
                "size": 768,
                "distance": "Cosine"
            }
        }
        r = requests.put(f"{QDRANT_HOST}/collections/{name}", json=payload)
        return jsonify(r.json()), r.status_code

    def insert_point(self, data):
        try:
            collection = data["collection"]
            question = data["question"]
            answer = data["answer"]
            unique_id = str(uuid.uuid4())
            vector = embed_service.get_embedding(question)
            payload = {
                "points": [
                    {
                        "id": unique_id,
                        "vector": vector,
                        "payload": {
                            "question": question,
                            "answer": answer
                        }
                    }
                ]
            }
            r = requests.put(f"{QDRANT_HOST}/collections/{collection}/points", json=payload)
            return jsonify(r.json()), r.status_code
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    def does_collection_exist(self, collection_name: str):
        try:
            response = requests.get(f"{QDRANT_HOST}/collections/{collection_name}")
            if response.status_code == 200:
                return True
            elif response.status_code == 404:
                return False
            else:
                raise Exception(f"Unexpected response from Qdrant: {response.text}")
        except Exception as e:
            raise Exception(f"Error checking collection existence: {str(e)}")  

    # def search_point(self, data):
    #     try:
    #         collection = data["collection"]
    #         query = data["query"]
    #         vector = embed_service.get_embedding(query)
    #         payload = {
    #             "vector": vector,
    #             "top": 5,
    #             "with_payload": True
    #         }
    #         r = requests.post(f"{QDRANT_HOST}/collections/{collection}/points/search", json=payload)
    #         return jsonify(r.json()), r.status_code
    #     except Exception as e:
    #         return jsonify({"error": str(e)}), 500


    def search_point(self, data):
        try:
            collection = data["collection"]
            query = data["query"]

            # Step 1: Get vector of user query
            vector = embed_service.get_embedding(query)

            # Step 2: Search top 5 points from Qdrant
            payload = {
                "vector": vector,
                "top": 5,
                "with_payload": True
            }
            r = requests.post(f"{QDRANT_HOST}/collections/{collection}/points/search", json=payload)

            if r.status_code != 200:
                return jsonify({"error": "Failed to search points", "details": r.json()}), r.status_code

            qdrant_points = r.json().get("result", [])

            # Step 3: Call helper to get human-like answer
            if not qdrant_points:
                return jsonify({
                    "user_question": query,
                    "human_like_answer": "0",
                    "msg": "No matched points found in Qdrant",
                    "top_points": []
                }), 200
            human_answer = get_human_like_answer(query, qdrant_points, self.gemini_service)

            print("DEBUG human_answer:", human_answer)
            # Step 4: Return both raw Qdrant results and human-like answer
            data = {
                "user_question": query,
                "human_like_answer": human_answer["answer"],
                "msg": "these are the matched points(questions) from qdrant",
                "top_points": qdrant_points
            }

            return Response(json.dumps(data, indent=2, ensure_ascii=False), mimetype="application/json")

        except Exception as e:
            return jsonify({"error": str(e)}), 500



    def get_questions_answers_paginated(self, collection_name: str, limit: int = 25, offset: str = None):
        try:
            # 1. Get total number of points in the collection
            stats_resp = requests.get(f"{QDRANT_HOST}/collections/{collection_name}")
            if stats_resp.status_code != 200:
                return jsonify({
                    "error": "Failed to fetch collection stats",
                    "details": stats_resp.json()
                }), stats_resp.status_code

            total_points = stats_resp.json().get("result", {}).get("points_count", 0)

            # 2. Prepare scroll payload
            payload = {
                "limit": limit,
                "with_payload": True,
                "with_vector": False
            }

            if offset:
                payload["offset"] = offset  # for pagination

            r = requests.post(f"{QDRANT_HOST}/collections/{collection_name}/points/scroll", json=payload)

            if r.status_code != 200:
                return jsonify({
                    "error": "Failed to fetch points",
                    "details": r.json()
                }), r.status_code

            result = r.json().get("result", {})
            points = result.get("points", [])
            next_page_offset = result.get("next_page_offset")  # important for pagination

            # 3. Extract Q&A
            qa_list = []
            for point in points:
                payload_data = point.get("payload", {})
                id = point.get("id")
                question = payload_data.get("question")
                answer = payload_data.get("answer")
                qa_list.append({
                    "id": id,
                    "question": question,
                    "answer": answer
                })

            # 4. Response with pagination info
            return jsonify({
                "total_points": total_points,
                "fetched": len(qa_list),
                "next_page_offset": next_page_offset,
                "qa_list": qa_list
            }), 200

        except Exception as e:
            return jsonify({"error": str(e)}), 500



    def delete_collection(self, collection_name: str):
        try:
            check = requests.get(f"{QDRANT_HOST}/collections/{collection_name}")
            if check.status_code == 404:
                return jsonify({"error": f"Collection '{collection_name}' not found in QDRANT Collection"}), 404

            response = requests.delete(f"{QDRANT_HOST}/collections/{collection_name}")
            return jsonify({"message": f"Collection '{collection_name}' removed successfully"}), 200

        except Exception as e:
            return jsonify({"error": str(e)}), 500


    def delete_questionById(self, collection_name: str, question_id: str):
        try:
            # 1. Check if the point exists by direct GET
            check_url = f"{QDRANT_HOST}/collections/{collection_name}/points/{question_id}"
            check = requests.get(check_url)

            if check.status_code == 404:
                return {
                    "error": f"Question with id '{question_id}' not found in collection '{collection_name}'"
                }, 404

            if check.status_code != 200:
                return {
                    "error": "Failed to fetch point",
                    "details": check.json()
                }, check.status_code

            # 2. Delete point by id
            delete_url = f"{QDRANT_HOST}/collections/{collection_name}/points/delete"
            delete_payload = {"points": [question_id]}
            response = requests.post(delete_url, json=delete_payload)

            if response.status_code == 200:
                return {
                    "message": f"Question with id '{question_id}' deleted successfully from collection '{collection_name}'"
                }, 200
            else:
                return {
                    "error": "Failed to delete point",
                    "details": response.json()
                }, response.status_code

        except Exception as e:
            return {"error": str(e)}, 500
        


    def bulk_qa_insert(self, qa_list: list, collection_name: str) -> Any:
        """Bulk insert multiple Q&A items into a Qdrant collection."""
        try:
            if not qa_list:
                return {"error": "No items provided"}, 400

            enriched_list = vectorize_qa_list(qa_list)
            points = []

            for item in enriched_list:
                points.append({
                    "id": str(uuid.uuid4()),
                    "vector": [float(v) for v in item.get("vector", [])],
                    "payload": {
                        "question": item.get("question"),
                        "answer": item.get("answer")
                    }
                })

            # Bulk insert all points in one request
            resp = requests.put(
                f"{QDRANT_HOST}/collections/{collection_name}/points",
                json={"points": points}
            )

            return {
                "inserted_count": len(points),
                "qdrant_response": resp.json() if resp.ok else resp.text
            }, resp.status_code

        except Exception as e:
            return {"error": str(e)}, 500
        

    def update_point(self, collection_name: str, point_id: str, question: str, answer: str) -> Any:
        """
        Overwrite an existing Q&A point in Qdrant with new vector + payload.
        Uses helper vectorize_qa_list to regenerate embeddings.
        """
        try:
            # Step 1: Build a temporary list for helper
            qa_list = [{"question": question, "answer": answer}]
            
            # Step 2: Generate new vector(s)
            enriched_list = vectorize_qa_list(qa_list)
            if not enriched_list:
                return {"error": "Failed to generate vector"}, 500

            new_vector = [float(v) for v in enriched_list[0].get("vector", [])]

            # Step 3: Prepare point overwrite (upsert)
            point = {
                "id": str(point_id),
                "vector": new_vector,
                "payload": {
                    "question": question,
                    "answer": answer
                }
            }

            # Step 4: Send upsert request
            url = f"{QDRANT_HOST}/collections/{collection_name}/points"
            resp = requests.put(url, json={"points": [point]})

            if resp.status_code == 200:
                return {
                    "success": True,
                    "message": f"Point {point_id} updated successfully in collection {collection_name}",
                    "qdrant_response": resp.json()
                }, 200
            else:
                return {
                    "success": False,
                    "error": "Failed to update point",
                    "details": resp.text
                }, resp.status_code

        except Exception as e:
            traceback.print_exc()
            return {"error": str(e)}, 500

    def get_total_qa(self, collection_name: str) -> Any:
        """
        Return total number of Q&A stored in a given collection.
        """
        try:
            resp = requests.get(f"{QDRANT_HOST}/collections/{collection_name}")
            
            if resp.status_code != 200:
                return {
                    "error": "Failed to fetch collection stats",
                    "details": resp.json()
                }, resp.status_code

            total_points = resp.json().get("result", {}).get("points_count", 0)

            return {
                "collection": collection_name,
                "total_qa": total_points
            }, 200

        except Exception as e:
            return {"error": str(e)}, 500
