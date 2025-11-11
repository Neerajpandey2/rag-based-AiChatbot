# rag-based-AiChatbot
A Retrieval-Augmented Generation (RAG) demo using Qdrant for vector search and a generative language model for answers. This repository contains the backend (Python/Flask) and a React frontend.

Repository layout
- Backend: [RAG-Qdrant-ChatAI-backend](.)
  - Main entry: [app.py](app.py)
  - Config: [config.py](config.py)
  - Logging: [logger.py](logger.py)
  - Requirements: [requirements.txt](requirements.txt)
  - Env file with service keys: [.env](.env) (DO NOT commit secrets)
  - Application package: [app/](app/)
  - Helpers: [helpers/](helpers/)
- Frontend: [RAG-Qdrant-ChatAI-frontend](../RAG-Qdrant-ChatAI-frontend)
  - Frontend config: [package.json](../RAG-Qdrant-ChatAI-frontend/package.json)
  - React sources: [../RAG-Qdrant-ChatAI-frontend/src](../RAG-Qdrant-ChatAI-frontend/src)

Quick start — Backend
1. Create a Python virtualenv and install deps:
   ```sh
   python -m venv venv
   source venv/bin/activate    # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   
2. Add environment variables:
Create a .env file in the backend root (see .env for the expected keys). Example (do NOT commit real keys):

  QDRANT_HOST=http://localhost:6333
  GEMINI_API_KEY=YOUR_API_KEY_HERE
  GEMINI_URL=https://generativelanguage.googleapis.com/v1beta/models/YOUR_MODEL:generateContent

3. Run the backend:
   python app.py

   -- The app uses the host from QDRANT_HOST and the generative API configured in .env.
Quick start — Frontend

From the repo root or backend folder, go to the frontend:
cd [RAG-Qdrant-ChatAI-frontend](http://_vscodecontentref_/0)
npm install
npm start

2. The React app will run (usually at http://localhost:3000) and communicate with the backend endpoints.
Architecture overview

The backend exposes endpoints under app/ (see routes/ inside) to:
Ingest documents (PDF helpers in helpers/pdf_helper.py)
Query the vector store (Qdrant) and produce answers using the generative model (helper code in helpers/get_humanLike_answer_helper.py)
Qdrant is used as the vector database (host configured via QDRANT_HOST in .env).
The frontend (React) provides the UI to interact with the chat and upload documents.
Security & publishing notes

Remove secrets before publishing. The repo currently contains a .env file — replace it with a .env.example or ensure .env is in .gitignore.
Rotate any API keys accidentally committed.
Do not commit large PDFs or private data.
Helpful files

Backend entry: app.py
Backend config: config.py
Dependency list: requirements.txt

Helpers: helpers/get_humanLike_answer_helper.py, helpers/pdf_helper.py
Frontend start: RAG-Qdrant-ChatAI-frontend/package.json
Logs: qa_log.json
Contributing

Create feature branches, open PRs, and ensure sensitive keys are not included.
Add tests or update the README with new endpoints if you add API surface.
License

Add a LICENSE file at the repo root if you want to apply a specific license.
If you want, I can:

Generate a .gitignore snippet to exclude .env and sensitive files.
Create a .env.example with placeholders.

