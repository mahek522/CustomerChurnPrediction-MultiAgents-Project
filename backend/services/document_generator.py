import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


def create_customer_documents(df):
    """
    Generate text documents from customer data for embedding.
    
    Args:
        df: Pandas DataFrame containing customer data
        
    Returns:
        list: List of text documents
    """
    documents = []
    metadatas = []
    
    for _, row in df.iterrows():
        # Handle churn status
        churn_status = "Churned" if row.get("churn", 0) == 1 else "Retained"
        
        text = f"""
        Customer {row.get('customer_id', 'Unknown')} is {row.get('age', 'Unknown')} years old.
        Tenure: {row.get('tenure_months', 'Unknown')} months.
        Monthly Charges: {row.get('monthly_charges', 'Unknown')}.
        Total Charges: {row.get('total_charges', 'Unknown')}.
        Contract Type: {row.get('contract_type', 'Unknown')}.
        Internet Service: {row.get('internet_service', 'Unknown')}.
        Support Tickets: {row.get('support_tickets', 'Unknown')}.
        Payment Method: {row.get('payment_method', 'Unknown')}.
        Customer Status: {churn_status}.
        """
        
        documents.append(text.strip())
        
        # Create metadata for filtering
        metadata = {
            "customer_id": str(row.get('customer_id', 'Unknown')),
            "age": str(row.get('age', 'Unknown')),
            "tenure_months": str(row.get('tenure_months', 'Unknown')),
            "churn": churn_status,
            "contract_type": str(row.get('contract_type', 'Unknown'))
        }
        metadatas.append(metadata)
    
    return documents, metadatas