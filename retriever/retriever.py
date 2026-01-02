from embeddings.embedder import embed_texts

def retrieve(query, store, chunks, k=5):
    query_embedding = embed_texts([query])[0]
    results = store.search(query_embedding, k)
    return results
