from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]

DATASET_PATH = BASE_DIR / "datasets" / "BNPParibas_Data.csv"

CHROMA_PATH = BASE_DIR / "database" / "chromadb"

POSTGRES_URL = "postgresql://postgres:Mahek123@localhost:5433/churn_memory_db"

CHROMA_COLLECTION_NAME = "customer_churn"

EMBEDDING_MODEL = "all-MiniLM-L6-v2"