import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from backend.services.config import CHROMA_PATH
import chromadb


def get_chroma_client():

    client = chromadb.PersistentClient(
        path=str(CHROMA_PATH)
    )

    return client