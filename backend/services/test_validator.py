from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

try:
    from backend.services.data_loader import load_dataset
    from backend.services.data_validator import validate_dataset
except ImportError:
    from data_loader import load_dataset
    from data_validator import validate_dataset


df = load_dataset()
valid, invalid = validate_dataset(df)
print("Valid Records:", len(valid))
print("Invalid Records:", len(invalid))
if invalid:
    print(invalid[:5])
