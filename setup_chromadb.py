"""
Setup script to initialize ChromaDB with customer data.
"""
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[0]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from backend.services.data_loader import load_dataset
from backend.services.data_cleaner import clean_dataset
from backend.services.document_generator import create_customer_documents
from backend.vectorstore.vector_ingestion import ingest_documents_to_chroma


def main():
    """Main setup function."""
    print("=" * 60)
    print("ChromaDB Setup for Customer Churn Intelligence Platform")
    print("=" * 60)
    print()
    
    # Step 1: Load dataset
    print("Step 1: Loading dataset...")
    try:
        df = load_dataset()
        print(f"  ✓ Dataset loaded: {df.shape[0]} rows, {df.shape[1]} columns")
    except Exception as e:
        print(f"  ✗ Error loading dataset: {e}")
        return
    
    # Step 2: Clean dataset
    print("\nStep 2: Cleaning dataset...")
    try:
        cleaned_df = clean_dataset(df)
        print(f"  ✓ Dataset cleaned: {cleaned_df.shape[0]} rows, {cleaned_df.shape[1]} columns")
    except Exception as e:
        print(f"  ✗ Error cleaning dataset: {e}")
        return
    
    # Step 3: Generate documents
    print("\nStep 3: Generating documents for embedding...")
    try:
        documents, metadatas = create_customer_documents(cleaned_df)
        print(f"  ✓ Generated {len(documents)} documents with metadata")
    except Exception as e:
        print(f"  ✗ Error generating documents: {e}")
        return
    
    # Step 4: Ingest into ChromaDB
    print("\nStep 4: Ingesting documents into ChromaDB...")
    try:
        result = ingest_documents_to_chroma((documents, metadatas))
        if result["status"] == "success":
            print(f"  ✓ Successfully ingested {result['documents_stored']} documents")
        else:
            print(f"  ✗ Error ingesting documents: {result.get('error')}")
            return
    except Exception as e:
        print(f"  ✗ Error during ingestion: {e}")
        return
    
    print("\n" + "=" * 60)
    print("ChromaDB Setup Complete! ✓")
    print("=" * 60)
    print()
    print("You can now:")
    print("  1. Start the backend: uvicorn backend.api.app:app --reload")
    print("  2. Start the frontend: streamlit run frontend/streamlit_app.py")
    print()


if __name__ == "__main__":
    main()
