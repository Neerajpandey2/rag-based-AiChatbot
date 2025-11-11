import PyPDF2
import io
import re
import json
import requests
from config import GEMINI_API_KEY, GEMINI_URL 
from typing import List, Dict, Any
from sentence_transformers import SentenceTransformer



# ---------------------------
# PDF Helpers
# ---------------------------

def validate_pdf_file(file):
    """Validate uploaded file type."""
    if not file.filename.lower().endswith(".pdf"):
        raise ValueError("Only PDF allowed")
    return file.read()


def extract_text_from_pdf(pdf_bytes):
    """Extract full text from PDF bytes."""
    reader = PyPDF2.PdfReader(io.BytesIO(pdf_bytes))
    full_text = ""
    for page in reader.pages:
        text = page.extract_text() or ""
        full_text += text + "\n"
    return full_text


def chunk_pdf_text(full_text):
    """Split text into chunks by headings (fallback: entire doc)."""
    lines = full_text.splitlines()
    chunks, current_content = [], []
    current_heading, found_heading = None, False

    for line in lines:
        line = line.strip()
        if (line.isupper() and len(line) > 3) or line.endswith(":") or (len(line) > 20 and line == line.title()):
            found_heading = True
            if current_content and current_heading:
                chunks.append({"heading": current_heading, "text": "\n".join(current_content)})
            current_heading, current_content = line, []
        else:
            current_content.append(line)

    if current_content and current_heading:
        chunks.append({"heading": current_heading, "text": "\n".join(current_content)})

    if not found_heading and full_text.strip():
        chunks = [{"heading": "Document", "text": full_text.strip()}]

    return chunks


# ---------------------------
# Gemini Helpers
# ---------------------------

def build_gemini_prompt(text):
    """Build a clean JSON-only instruction prompt for Gemini."""
    return f"""
    You are a Q&A extractor.

    Given the following text:

    ---
    {text}
    ---

    Extract ALL possible question and answer pairs from the text.

    Return them strictly in JSON array format like this:
    [
    {{"question": "<q1>", "answer": "<a1>"}},
    {{"question": "<q2>", "answer": "<a2>"}},
    ...
    ]

    Rules:
    - Include as many Q&A pairs as are reasonably supported by the text.
    - Do not add explanations, markdown, or extra text.
    - Return only valid JSON.
    """


def call_gemini_api(prompt):
    """Send request to Gemini and return raw response text & parsed data."""
    headers = {
        "Content-Type": "application/json",
        "X-goog-api-key": GEMINI_API_KEY
    }
    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    resp = requests.post(GEMINI_URL, headers=headers, json=payload, timeout=60)
    raw_text = resp.text
    try:
        data = resp.json()
    except Exception:
        data = None
    return resp.status_code, raw_text, data


def parse_gemini_response(data, raw_text, chunk_text):
    """Extract Q&A pairs from Gemini response or fallback."""
    if not data:
        return [{"question": chunk_text[:50], "answer": ""}]

    try:
        answer_text = data["candidates"][0]["content"]["parts"][0]["text"]
    except Exception:
        answer_text = ""

    # Clean markdown fences
    answer_text = answer_text.strip()
    if answer_text.startswith("```"):
        answer_text = re.sub(r"^```[a-zA-Z]*\n?", "", answer_text)
        answer_text = re.sub(r"```$", "", answer_text).strip()

    try:
        return json.loads(answer_text)
    except json.JSONDecodeError:
        return [{"question": chunk_text[:50], "answer": answer_text}]


# ---------------------------
# Vectorization Helper
# ---------------------------

_embedding_model = SentenceTransformer("sentence-transformers/all-mpnet-base-v2")

def vectorize_qa_list(qa_list: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Vectorize a list of Q/A pairs into embeddings.

    Args:
        qa_list: List of dicts with keys:
            - "question" (str)
            - "answer" (str)

    Returns:
        List of dicts with keys:
            - "question"
            - "answer"
            - "vector" (list[float])
    """
    if not qa_list:
        return []

    # Extract questions
    questions = [item.get("question", "") for item in qa_list]

    # Get embeddings
    vectors = _embedding_model.encode(questions).tolist()

    # Build enriched response
    enriched = []
    for item, vec in zip(qa_list, vectors):
        enriched.append({
            "question": item.get("question"),
            "answer": item.get("answer"),
            "vector": vec   #key aligned with your route/swagger
        })

    return enriched
  
