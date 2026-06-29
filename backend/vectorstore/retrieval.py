import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from backend.vectorstore.collection_manager import get_collection
from backend.vectorstore.embedding_service import generate_embeddings

def retrieve_documents(query: str, top_k: int = 5):
    """
    Retrieve the most relevant customer records from ChromaDB.
    """
    try:
        collection = get_collection()
        query_embedding = generate_embeddings([query])[0]
        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k
        )
        return results
    except Exception as e:
        print(f"Error during document retrieval: {e}")
        return {"documents": [[]], "metadatas": [[]]}