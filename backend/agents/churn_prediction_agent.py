from pathlib import Path
import sys
import os

ROOT = Path(__file__).resolve().parents[2]

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from crewai import Agent
from backend.agents.llm_config import llm, USE_MOCK_MODE

from backend.tools.retrieval_tool import brave_search

if USE_MOCK_MODE:
    churn_prediction_agent = Agent(
        role="Customer Churn Prediction Expert",
        goal="""
        Predict which customers are most likely to churn. Do NOT call any tools.
        """,
        backstory="""
        Banking churn prediction specialist. No tools allowed.
        """,
        llm=None,
        verbose=False,
    )
else:
    churn_prediction_agent = Agent(
        role="Customer Churn Prediction Expert",
        goal="""
        Predict which customers are most likely to churn. Estimate risk level and explain why.
        CRITICAL: Do NOT call any tools or functions (such as brave_search). You have NO tools.
        """,
        backstory="""
        You are a banking churn prediction specialist. You analyze retrieved customer records and classify
        customers into Low Risk, Medium Risk, or High Risk.
        You rely solely on provided data. Never output any tool calls, function calls, or web searches.
        """,
        tools=[brave_search],
        verbose=False,
        llm=llm
    )