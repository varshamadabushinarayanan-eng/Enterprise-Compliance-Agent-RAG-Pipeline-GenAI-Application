from pathlib import Path
import os
from dotenv import load_dotenv
from openai import OpenAI
import chromadb

ROOT = Path(__file__).resolve().parents[1]
load_dotenv(ROOT/".env")
API_KEY = os.getenv("OPENAI_API_KEY")
if not API_KEY:
    raise RuntimeError("Set OPENAI_API_KEY in the project's .env file.")
client = OpenAI(api_key=API_KEY)
CHAT_MODEL = os.getenv("OPENAI_CHAT_MODEL","gpt-4o-mini")
EMBED_MODEL = os.getenv("OPENAI_EMBEDDING_MODEL","text-embedding-3-small")
DB_DIR = ROOT/"chroma_db"
COLLECTION = "mock_compliance_docs"

def get_collection():
    db = chromadb.PersistentClient(path=str(DB_DIR))
    return db.get_or_create_collection(COLLECTION, metadata={"hnsw:space":"cosine"})

def embed(texts):
    response = client.embeddings.create(model=EMBED_MODEL, input=texts)
    return [item.embedding for item in response.data]
