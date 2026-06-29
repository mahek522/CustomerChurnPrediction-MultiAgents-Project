from pydantic import BaseModel
from typing import List

class ReportOutput(BaseModel):
    executive_summary: str
    key_findings: List[str]
    recommendations: List[str]
    confidence_score: float