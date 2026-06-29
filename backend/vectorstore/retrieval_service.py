import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from backend.vectorstore.collection_manager import get_collection
from backend.vectorstore.embedding_service import generate_embeddings


def retrieve_context(query: str, n_results: int = 5):
    collection = get_collection()
    query_embedding = generate_embeddings([query])
    results = collection.query(
        query_embeddings=query_embedding,
        n_results=n_results
    )
    return results