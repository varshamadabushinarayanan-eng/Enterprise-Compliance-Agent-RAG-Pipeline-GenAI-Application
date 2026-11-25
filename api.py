from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from rag import answer_question

app = FastAPI(title="Mock Enterprise Compliance RAG Assistant", version="1.0")

class AskRequest(BaseModel):
    question: str = Field(min_length=5, max_length=2000)
    top_k: int = Field(default=4, ge=1, le=8)

@app.get("/")
def home():
    return {"message":"Mock compliance RAG demo","docs":"/docs"}

@app.post("/ask")
def ask(payload: AskRequest):
    try:
        return answer_question(payload.question, payload.top_k)
    except Exception as exc:
        raise HTTPException(status_code=503, detail=str(exc))
