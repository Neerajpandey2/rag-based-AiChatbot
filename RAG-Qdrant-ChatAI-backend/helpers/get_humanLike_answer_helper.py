# app/helpers/gemini_helper.py
from app.services.askGemini_service import GeminiService

def get_human_like_answer(user_question: str, qdrant_points: list, gemini_service: GeminiService):
    """
    Takes user question and Qdrant search points, sends a prompt to Gemini to get a human-like answer.
    """
    # Step 1: Format Qdrant points into readable Q&A
    formatted = ""
    for i, point in enumerate(qdrant_points, 1):
        q = point["payload"].get("question", "")
        a = point["payload"].get("answer", "")
        formatted += f"{i}. Q: {q}\n   A: {a}\n"

    # Step 2: Build prompt for Gemini
    prompt = (
        "You are a helpful AI assistant. Based on the following Q&A pairs, "
        "answer the user's question in a clear, human-like way. if the answer is not clear then just send single 0. thats it no more text just 0\n\n"
        f"{formatted}\n"
        f"User Question: {user_question}\n"
        "Answer:"
    )

    # Step 3: Call Gemini service directly (not the Flask route)
    result = gemini_service.ask(prompt)
    return {"answer": result['answer']}
