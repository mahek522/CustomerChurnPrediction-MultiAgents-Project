import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from sentence_transformers import SentenceTransformer

from backend.services.config import EMBEDDING_MODEL

try:
    model = SentenceTransformer(EMBEDDING_MODEL)
except Exception as e:
    print(f"Error loading embedding model: {e}")
    model = None


def generate_embeddings(texts):
    if model is None:
        raise RuntimeError("Embedding model not loaded")
    try:
        embeddings = model.encode(texts, show_progress_bar=True)
        return embeddings.tolist()
    except Exception as e:
        print(f"Error generating embeddings: {e}")
        raise