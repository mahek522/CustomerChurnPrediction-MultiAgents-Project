from pydantic import BaseModel
from typing import List

class ChurnPredictionOutput(BaseModel):
    risk_level: str
    confidence_score: float
    churn_factors: List[str]
    evidence: List[str]
    reasoning_summary: str