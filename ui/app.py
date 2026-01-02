import streamlit as st
import requests

st.set_page_config(page_title="Codebase RAG Assistant")

st.title("Codebase RAG Assistant")
st.write("Semantic search over large codebases")

BACKEND_URL = "http://localhost:8001"

# ------------------------------
# Ingest Repository
# ------------------------------
st.subheader("1️⃣ Ingest GitHub Repository")

repo_url = st.text_input("Enter GitHub Repository URL")

if st.button("Ingest Repository"):
    if repo_url:
        res = requests.post(
            f"{BACKEND_URL}/ingest",
            json={"repo_url": repo_url}
        )
        st.json(res.json())
    else:
        st.warning("Please enter a repository URL")

# ------------------------------
# Search Code
# ------------------------------
st.subheader("2️⃣ Ask Questions About the Code")

query = st.text_input("Enter your question (e.g., authentication, routing, database)")

if st.button("Search Code"):
    if query:
        res = requests.post(
            f"{BACKEND_URL}/search",
            json={"query": query}
        )

        data = res.json()

        if "results" in data:
            for i, result in enumerate(data["results"], 1):
                st.markdown(f"**Result {i}:** `{result['path']}`")
        else:
            st.json(data)
    else:
        st.warning("Please enter a query")