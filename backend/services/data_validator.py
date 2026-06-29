from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

try:
    from backend.schemas.customer_schema import CustomerSchema
except ImportError:
    from schemas.customer_schema import CustomerSchema


def validate_dataset(df):
    valid_records = []
    invalid_records = []
    for index, row in df.iterrows():
        try:
            customer = CustomerSchema(**row.to_dict())
            valid_records.append(customer.model_dump())
        except Exception as e:
            invalid_records.append(
                {
                    "row": index,
                    "error": str(e),
                }
            )

    return valid_records, invalid_records