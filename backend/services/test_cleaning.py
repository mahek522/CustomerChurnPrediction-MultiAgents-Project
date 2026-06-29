from data_loader import load_dataset
from data_cleaner import clean_dataset

df = load_dataset()
print("Before:", df.shape)
df = clean_dataset(df)
print("After:", df.shape)