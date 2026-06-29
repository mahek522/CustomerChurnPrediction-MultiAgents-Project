import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from backend.services.data_cleaner import clean_dataset
from backend.services.data_loader import load_dataset
from backend.services.document_generator import create_customer_documents
from backend.vectorstore.vector_ingestion import ingest_documents_to_chroma


class DataIngestionPipeline:
    """Complete data ingestion pipeline for customer churn data."""
    
    def __init__(self):
        self.dataset_path = None
    
    def ingest_dataset(self, df):
        """
        Ingest a pandas DataFrame into ChromaDB.
        
        Args:
            df: Pandas DataFrame containing customer data
            
        Returns:
            dict: Summary of ingestion results
        """
        try:
            # Clean the data
            cleaned_df = clean_dataset(df)
            
            # Generate documents for each customer
            documents = create_customer_documents(cleaned_df)
            
            # Ingest into ChromaDB
            result = ingest_documents_to_chroma(documents)
            
            return {
                "status": "success",
                "records_processed": len(cleaned_df),
                "documents_created": len(documents),
                "collection_name": "customer_churn"
            }
        except Exception as e:
            return {
                "status": "error",
                "error": str(e)
            }
    
    def run_from_file(self, dataset_path):
        """
        Run ingestion from a CSV file.
        
        Args:
            dataset_path: Path to CSV file
            
        Returns:
            dict: Summary of ingestion results
        """
        self.dataset_path = dataset_path
        df = load_dataset(dataset_path)
        return self.ingest_dataset(df)


def run_ingestion():
    """Legacy function for backward compatibility."""
    pipeline = DataIngestionPipeline()
    return pipeline.run_from_file(None)
