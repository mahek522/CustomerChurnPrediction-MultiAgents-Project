from data_loader import load_dataset
from document_generator import create_customer_documents

df = load_dataset()

documents = create_customer_documents(df)

print(documents[0])