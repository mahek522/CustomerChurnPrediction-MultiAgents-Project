import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import pandas as pd


def clean_dataset(df):
    """
    Clean the dataset by removing duplicates, null values, and standardizing text.
    
    Args:
        df: Pandas DataFrame to clean
        
    Returns:
        pd.DataFrame: Cleaned DataFrame
    """
    # Remove duplicates
    df = df.drop_duplicates()
    
    # Remove null rows
    df = df.dropna()
    
    # Strip text columns if they exist
    text_columns = [
        "contract_type",
        "internet_service",
        "payment_method"
    ]
    
    for col in text_columns:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip()
    
    return df