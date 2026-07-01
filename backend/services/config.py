import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]

DATASET_PATH = BASE_DIR / "datasets" / "BNPParibas_Data.csv"

CHROMA_PATH = BASE_DIR / "database" / "chromadb"

raw_url = os.getenv("DATABASE_URL") or os.getenv("POSTGRES_URL") or "postgresql://postgres:Mahek123@localhost:5433/churn_memory_db"

# SQLAlchemy 1.4+ requires postgresql:// instead of postgres://
if raw_url and raw_url.startswith("postgres://"):
    raw_url = raw_url.replace("postgres://", "postgresql://", 1)

POSTGRES_URL = raw_url

CHROMA_COLLECTION_NAME = "customer_churn"

EMBEDDING_MODEL = "all-MiniLM-L6-v2"