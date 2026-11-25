"""Optional basic MLflow logging for a single RAG question/response run."""
import mlflow
from rag import answer_question

mlflow.set_experiment("mock-enterprise-compliance-rag")
question = "What evidence should be retained during a data integrity record review?"
with mlflow.start_run():
    result = answer_question(question)
    mlflow.log_param("top_k", 4)
    mlflow.log_param("chat_model", "configured via OPENAI_CHAT_MODEL")
    mlflow.log_metric("retrieved_chunks", result["retrieved_chunks"])
    mlflow.log_text(question, "question.txt")
    mlflow.log_text(result["answer"], "answer.txt")
    mlflow.log_text("\n".join(result["sources"]), "sources.txt")
    print(result["answer"])
