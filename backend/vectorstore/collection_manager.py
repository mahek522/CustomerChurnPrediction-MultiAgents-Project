import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from backend.vectorstore.chroma_client import get_chroma_client
from backend.services.config import CHROMA_COLLECTION_NAME


def get_collection():

    client = get_chroma_client()

    collection = client.get_or_create_collection(
        name=CHROMA_COLLECTION_NAME
    )

    return collection