"""Optional LangGraph workflow wrapper around the RAG function."""
from typing import TypedDict
from langgraph.graph import StateGraph, END
from rag import answer_question

class State(TypedDict):
    question: str
    result: dict

def retrieve_and_answer(state: State):
    return {"result": answer_question(state["question"])}

graph = StateGraph(State)
graph.add_node("retrieve_and_answer", retrieve_and_answer)
graph.set_entry_point("retrieve_and_answer")
graph.add_edge("retrieve_and_answer", END)
app = graph.compile()

if __name__ == "__main__":
    output = app.invoke({"question":"What details are listed as required fields for a deviation?", "result":{}})
    print(output["result"]["answer"])
