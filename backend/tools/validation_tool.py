import json
import sys
import os
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from crewai.tools import tool
from pydantic import BaseModel
from pydantic_ai import Agent as PydanticAIAgent
from backend.schemas.validation_schema import ValidationSchema

# Configure Pydantic AI
USE_MOCK_MODE = os.getenv("USE_MOCK_MODE", "false").lower() == "true"
USE_OLLAMA = os.getenv("USE_OLLAMA", "true").lower() == "true"

def get_pydantic_ai_agent():
    if USE_MOCK_MODE:
        class MockAgent:
            def run_sync(self, prompt: str):
                class MockResult:
                    def __init__(self):
                        # Use is_valid=False if low evidence is requested to simulate policy rules
                        is_low = "insufficient" in prompt.lower() or "low evidence" in prompt.lower()
                        self.data = ValidationSchema(
                            is_valid=not is_low,
                            confidence_score=0.50 if is_low else 0.95,
                            validation_notes="Mock validation completed. Grounded in provided customer records."
                        )
                return MockResult()
        return MockAgent()
    
    # Select Pydantic AI Model
    if USE_OLLAMA:
        model_name = "ollama:llama3.2"
    else:
        # Pydantic AI groq model can be initialized via string
        model_name = "groq:llama-3.1-8b-instant"
        
    return PydanticAIAgent(
        model_name,
        result_type=ValidationSchema,
        system_prompt=(
            "You are a validation specialist. Your task is to validate a user segment/churn analysis "
            "and recommendation report. Return a structured validation response matching ValidationSchema.\n"
            "Follow these business policies: \n"
            "1. Grounding: Verify claims are supported by dataset records.\n"
            "2. Hallucinations: If the report contains forbidden terms like 'logistic regression', "
            "'coefficient', 'balance level', or 'payment history', flag them and set is_valid=False.\n"
            "3. Confidence: Estimate a confidence score from 0.0 to 1.0. If the confidence is below 0.70 (70%), "
            "set is_valid=False and validation_notes to include 'Insufficient Evidence'.\n"
            "4. Numerical: Statistical calculations must be verified."
        )
    )

@tool("Grounding Validation Tool")
def validate_grounding(response: str) -> str:
    """
    Validate whether the generated response contains unsupported claims,
    hallucinated information or fails validation policies using Pydantic AI.
    Returns a JSON string of the ValidationSchema output.
    """
    try:
        agent = get_pydantic_ai_agent()
        prompt = f"Please validate the following report:\n\n{response}"
        result = agent.run_sync(prompt)
        
        # Additional rule check for forbidden terms (as extra guardrail)
        forbidden = [
            "logistic regression",
            "coefficient",
            "balance level",
            "payment history",
        ]
        
        is_valid = result.data.is_valid
        confidence_score = result.data.confidence_score
        validation_notes = result.data.validation_notes
        
        found_forbidden = [f for f in forbidden if f.lower() in response.lower()]
        if found_forbidden:
            is_valid = False
            validation_notes = f"Failed validation: contains forbidden terms {found_forbidden}. " + validation_notes
            
        if confidence_score < 0.70:
            is_valid = False
            validation_notes = "Insufficient Evidence. - " + validation_notes
            
        schema_output = ValidationSchema(
            is_valid=is_valid,
            confidence_score=confidence_score,
            validation_notes=validation_notes
        )
        
        return json.dumps(schema_output.model_dump())
    except Exception as e:
        # Fallback to simple parser on failure
        return json.dumps({
            "is_valid": False,
            "confidence_score": 0.0,
            "validation_notes": f"Validation failed with error: {str(e)}"
        })