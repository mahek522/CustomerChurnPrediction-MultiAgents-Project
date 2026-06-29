import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from backend.schemas.churn_prediction_schema import ChurnPredictionOutput
def analyze_customer():
    result = ChurnPredictionOutput(
        risk_level="High",
        confidence_score=87.5,
        churn_factors=[
            "High monthly charges",
            "Short tenure"
        ],
        evidence=[
            "Customer 101",
            "Customer 205"
        ],
        reasoning_summary=
        "Customers with high monthly charges and short tenure show higher churn risk."
    )
    return result