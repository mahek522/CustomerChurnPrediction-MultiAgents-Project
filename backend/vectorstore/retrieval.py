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
    Falls back to loading directly from the CSV if database or embeddings fail.
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
        print(f"Warning: Semantic retrieval failed ({e}). Falling back to local CSV records.")
        try:
            import pandas as pd
            from backend.services.config import DATASET_PATH
            import re
            
            if not DATASET_PATH.exists():
                print(f"DATASET_PATH {DATASET_PATH} does not exist.")
                return {"documents": [[]], "metadatas": [[]]}
                
            df = pd.read_csv(DATASET_PATH)
            # Find specific customer IDs (e.g. 1234 or containing digits)
            digits = re.findall(r"\b\d{3,6}\b", query)
            matched_df = pd.DataFrame()
            
            if digits:
                for d in digits:
                    match = df[df['customer_id'].astype(str).str.contains(d)]
                    if not match.empty:
                        matched_df = pd.concat([matched_df, match])
            
            # Fallback to top_k records if no match or not found
            if matched_df.empty:
                matched_df = df.head(top_k)
            else:
                matched_df = matched_df.head(top_k)
                
            # Format results in ChromaDB style
            documents = []
            metadatas = []
            for _, row in matched_df.iterrows():
                doc_str = ", ".join([f"{col}: {val}" for col, val in row.items()])
                documents.append(doc_str)
                metadatas.append({"source": "csv_fallback"})
                
            return {
                "documents": [documents],
                "metadatas": [metadatas]
            }
        except Exception as fallback_err:
            print(f"Fallback CSV reading failed: {fallback_err}")
            return {"documents": [[]], "metadatas": [[]]}