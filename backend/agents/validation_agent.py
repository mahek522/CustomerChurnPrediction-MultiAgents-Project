from pathlib import Path
import sys
import os

ROOT = Path(__file__).resolve().parents[2]

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from crewai import Agent
from backend.agents.llm_config import llm, USE_MOCK_MODE
from backend.tools.validation_tool import validate_grounding

if USE_MOCK_MODE:
    validation_agent = Agent(
        role="Validation Specialist",
        goal="""
        Validate all outputs produced by previous agents.
        Ensure recommendations are supported by evidence
        and remove hallucinations.
        """,
        backstory="""
        You verify that every prediction and recommendation is supported
        by retrieved customer data and prior analysis.
        Use the Grounding Validation Tool to flag unsupported claims.
        """,
        tools=[validate_grounding],
        llm=None,
        verbose=False,
    )
else:
    validation_agent = Agent(
        role="Validation Specialist",
        goal="""
        Validate all outputs produced by previous agents.
        Ensure recommendations are supported by evidence
        and remove hallucinations.
        """,
        backstory="""
        You verify that every prediction and recommendation is supported
        by retrieved customer data and prior analysis.
        Use the Grounding Validation Tool to flag unsupported claims.
        """,
        tools=[validate_grounding],
        verbose=False,
        llm=llm,
    )
