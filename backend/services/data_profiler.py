from data_loader import load_dataset

df = load_dataset()

print("\nRows, Columns")
print(df.shape)

print("\nMissing Values")
print(df.isnull().sum())

print("\nData Types")
print(df.dtypes)

print("\nStatistics")
print(df.describe())