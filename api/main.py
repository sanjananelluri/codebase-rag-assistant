from fastapi import FastAPI
from ingestion.repo_loader import clone_repo, read_code_files

from embeddings.chunker import chunk_code_files
from embeddings.embedder import embed_texts
from vector_store.faiss_store import FAISSStore

app = FastAPI()

# Global objects (simple MVP approach)
store = None
chunks_cache = None


@app.post("/ingest")
def ingest_repo(data: dict):
    global store, chunks_cache

    repo_url = data.get("repo_url")
    if not repo_url:
        return {"error": "repo_url is required"}

    # 1. Clone + read files
    repo_path = clone_repo(repo_url)
    files = read_code_files(repo_path)

    # 2. Chunk code
    chunks = chunk_code_files(files)

    if not chunks:
        return {"error": "No code files found"}

    # 3. Create embeddings
    texts = [c["text"] for c in chunks]
    metadatas = [c["metadata"] for c in chunks]

    embeddings = embed_texts(texts)

    # 4. Build vector store
    store = FAISSStore(len(embeddings[0]))
    store.add(embeddings, metadatas)

    chunks_cache = chunks

    return {
        "message": "Repository ingested successfully",
        "files_count": len(files),
        "chunks_count": len(chunks)
    }


@app.post("/search")
def search_code(data: dict):
    if store is None:
        return {"error": "Repository not ingested yet"}

    query = data.get("query")
    if not query:
        return {"error": "query is required"}

    query_embedding = embed_texts([query])[0]
    results = store.search(query_embedding, k=5)

    return {
        "query": query,
        "results": results
    }