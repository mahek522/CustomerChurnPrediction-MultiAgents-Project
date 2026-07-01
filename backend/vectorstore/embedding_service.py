import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from backend.services.config import EMBEDDING_MODEL

_model = None

def get_model():
    global _model
    if _model is None:
        print("Lazy loading SentenceTransformer embedding model...")
        from sentence_transformers import SentenceTransformer
        from backend.services.config import EMBEDDING_MODEL
        try:
            _model = SentenceTransformer(EMBEDDING_MODEL)
        except Exception as e:
            print(f"Error loading embedding model: {e}")
            _model = None
    return _model


def generate_embeddings(texts):
    model = get_model()
    if model is None:
        raise RuntimeError("Embedding model not loaded")
    try:
        embeddings = model.encode(texts, show_progress_bar=False)
        return embeddings.tolist()
    except Exception as e:
        print(f"Error generating embeddings: {e}")
        raise