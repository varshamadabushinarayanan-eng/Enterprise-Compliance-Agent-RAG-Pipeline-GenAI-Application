from pathlib import Path
from common import ROOT, get_collection, embed

DOC_DIR = ROOT/"documents"
collection = get_collection()
ids, texts, metas = [], [], []
for path in sorted(DOC_DIR.glob("*.md")):
    content = path.read_text(encoding="utf-8")
    # Simple paragraph-based chunking for transparent demonstration.
    paragraphs = [p.strip() for p in content.split("\n\n") if p.strip()]
    for i, paragraph in enumerate(paragraphs):
        ids.append(f"{path.stem}-{i}")
        texts.append(paragraph)
        metas.append({"source":path.name,"chunk":i})
if not texts:
    raise RuntimeError("No markdown documents found in documents/")
vectors = embed(texts)
# Rebuild collection contents so repeated ingestion doesn't create stale chunks.
existing = collection.get()
if existing.get("ids"):
    collection.delete(ids=existing["ids"])
collection.add(ids=ids, documents=texts, metadatas=metas, embeddings=vectors)
print(f"Indexed {len(texts)} chunks from {len(list(DOC_DIR.glob('*.md')))} mock documents.")
