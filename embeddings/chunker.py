def chunk_code_files(code_files):
    chunks = []

    for file in code_files:
        chunks.append({
            "text": file["content"],
            "metadata": {
                "path": file["path"]
            }
        })

    return chunks