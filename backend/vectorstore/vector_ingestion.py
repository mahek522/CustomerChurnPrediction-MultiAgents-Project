import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from backend.vectorstore.embedding_service import generate_embeddings
from backend.vectorstore.collection_manager import get_collection


def ingest_documents_to_chroma(documents_with_metadata):
    """
    Ingest documents into ChromaDB with embeddings.
    
    Args:
        documents_with_metadata: Either a list of documents or tuple of (documents, metadatas)
        
    Returns:
        dict: Summary of ingestion results
    """
    try:
        # Handle both old format (documents only) and new format (documents, metadatas)
        if isinstance(documents_with_metadata, tuple) and len(documents_with_metadata) == 2:
            documents, metadatas = documents_with_metadata
        else:
            documents = documents_with_metadata
            metadatas = [{"source": "customer_dataset"} for _ in documents]
        
        # Generate embeddings
        embeddings = generate_embeddings(documents)
        
        # Get or create collection
        collection = get_collection()
        
        # Generate IDs
        ids = [str(i) for i in range(len(documents))]
        
        # Add to collection
        collection.add(
            ids=ids,
            documents=documents,
            embeddings=embeddings,
            metadatas=metadatas
        )
        
        print(f"{len(documents)} documents stored in ChromaDB")
        
        return {
            "status": "success",
            "documents_stored": len(documents)
        }
    except Exception as e:
        print(f"Error ingesting documents: {e}")
        return {
            "status": "error",
            "error": str(e)
        }


def ingest_documents():
    """Legacy function for backward compatibility."""
    from backend.services.data_ingestion_pipeline import run_ingestion
    documents = run_ingestion()
    return ingest_documents_to_chroma(documents)