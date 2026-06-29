from pydantic import BaseModel

class ValidationSchema(BaseModel):
    is_valid: bool
    confidence_score: float
    validation_notes: str