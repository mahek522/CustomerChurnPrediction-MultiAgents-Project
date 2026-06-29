from data_ingestion_pipeline import run_ingestion

documents = run_ingestion()
print()
print("Generated Documents")
print(len(documents))