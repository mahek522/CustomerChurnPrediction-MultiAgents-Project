from pydantic import BaseModel
from typing import Literal

class CustomerSchema(BaseModel):
    customer_id: int
    age: int
    tenure_months: int
    monthly_charges: float
    total_charges: float
    contract_type: str
    internet_service: str
    support_tickets: int
    payment_method: str
    churn: int