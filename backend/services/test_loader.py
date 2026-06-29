try:
    from .data_loader import load_dataset
except ImportError:
    from data_loader import load_dataset


df = load_dataset()

print(df.head())