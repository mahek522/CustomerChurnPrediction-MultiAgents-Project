"""
Deterministic customer record retrieval from ChromaDB.

Retrieval is a pure Python operation (embed + vector search).
It must never invoke an LLM.
"""
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from backend.vectorstore.retrieval import retrieve_documents


def retrieve_customer_records(query: str, top_k: int = 5) -> str:
    """
    Retrieve and format customer records for downstream agents.
    """
    try:
        results = retrieve_documents(query, top_k=top_k)
        if not results or not results.get("documents") or not results["documents"][0]:
            return "No records found."

        docs = results["documents"][0]
        metadatas = results.get("metadatas", [[]])[0] if results.get("metadatas") else []

        formatted = []
        for index, doc in enumerate(docs):
            header = f"--- Record {index + 1} ---"
            if index < len(metadatas) and metadatas[index]:
                header = f"--- Record {index + 1} (metadata: {metadatas[index]}) ---"
            formatted.append(f"{header}\n{doc}")

        return "\n\n".join(formatted)
    except Exception as e:
        return f"Error during retrieval: {str(e)}"
