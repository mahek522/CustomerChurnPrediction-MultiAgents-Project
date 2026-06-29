from pydantic import BaseModel
from typing import List

class RecommendationOutput(BaseModel):
    recommendations: List[str]
    priority: str
    expected_impact: str