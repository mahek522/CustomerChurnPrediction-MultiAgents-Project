import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from backend.services.config import DATASET_PATH
import pandas as pd


def load_dataset(dataset_path=None):
    """
    Load dataset from CSV file.
    
    Args:
        dataset_path: Path to CSV file. If None, uses default DATASET_PATH
        
    Returns:
        pd.DataFrame: Loaded dataset
    """
    path = dataset_path or DATASET_PATH
    df = pd.read_csv(path)
    print(f"Dataset loaded successfully: {df.shape}")
    return df