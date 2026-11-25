# Project 2 — Enterprise Compliance Agent: RAG Pipeline & GenAI Application

## What this demonstrates
A small retrieval-augmented generation (RAG) demo that:
- loads mock SOP/policy documents from `documents/`;
- splits documents into searchable chunks;
- creates embeddings and stores them in ChromaDB;
- retrieves relevant chunks for a question;
- sends retrieved context to an LLM to draft a grounded answer;
- exposes a FastAPI endpoint;
- includes an optional LangGraph workflow and MLflow experiment logging.

## Important source note
All files in `documents/` are **fictional training examples**, not official regulations, not approved SOPs, and not company-controlled documents. This demo is not a substitute for regulatory interpretation, QA approval, or validated GxP software. Do not upload confidential or patient information.

## Setup
Requires Python 3.10+ and an OpenAI API key with API access.
```bash
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
cp .env.example .env
# Add your OPENAI_API_KEY to .env
python src/ingest.py
uvicorn src.api:app --reload
```
Open `http://127.0.0.1:8000/docs`.

## Ask a question
POST `/ask`:
```json
{"question":"What information should be captured when documenting a deviation?"}
```

## Optional LangGraph + MLflow
```bash
python src/langgraph_demo.py
python src/mlflow_tracking.py
mlflow ui
```
LangGraph and MLflow are optional demonstrations. The core ingestion and API use the OpenAI SDK and ChromaDB directly for easier inspection.
