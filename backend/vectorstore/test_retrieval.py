import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from backend.vectorstore.retrieval import retrieve_documents

results = retrieve_documents(
    "customers with high monthly charges"
)

print(results)