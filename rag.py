from common import client, CHAT_MODEL, get_collection, embed

def answer_question(question: str, top_k: int = 4):
    collection = get_collection()
    if collection.count() == 0:
        raise RuntimeError("Vector index is empty. Run: python src/ingest.py")
    query_vector = embed([question])[0]
    hits = collection.query(query_embeddings=[query_vector], n_results=min(top_k, collection.count()))
    docs = hits.get("documents", [[]])[0]
    metas = hits.get("metadatas", [[]])[0]
    context = "\n\n".join(
        f"[Source: {meta.get('source')} | chunk {meta.get('chunk')}]\n{doc}"
        for doc, meta in zip(docs, metas)
    )
    system = (
        "You are a cautious document-assistance tool. Answer only from the supplied context. "
        "If the context does not contain the answer, say that the indexed mock documents do not specify it. "
        "Clearly identify this as training content, not regulatory or quality approval."
    )
    response = client.chat.completions.create(
        model=CHAT_MODEL,
        temperature=0.1,
        messages=[
            {"role":"system","content":system},
            {"role":"user","content":f"Question: {question}\n\nRetrieved context:\n{context}\n\nGive a concise answer and list the source filenames."}
        ]
    )
    return {"answer":response.choices[0].message.content,
            "sources":sorted({m.get("source","unknown") for m in metas}),
            "retrieved_chunks":len(docs),
            "disclaimer":"Fictional training documents only; not regulatory advice or an approved quality decision."}
