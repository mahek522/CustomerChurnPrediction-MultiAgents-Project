from pathlib import Path
import sys
import os

ROOT = Path(__file__).resolve().parents[2]

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from crewai import Agent
from backend.agents.llm_config import llm, USE_MOCK_MODE

if USE_MOCK_MODE:
    churn_prediction_agent = Agent(
        role="Customer Churn Prediction Expert",
        goal="""
        Predict which customers are most likely to churn.
        Estimate risk level and explain why.
        """,
        backstory="""
        You are a banking churn prediction specialist.
        You analyze retrieved customer records and classify
        customers into
        • Low Risk
        • Medium Risk
        • High Risk
        You always explain the reasons behind the prediction.
        """,
        llm=None,
        verbose=False,
    )
else:
    churn_prediction_agent = Agent(
        role="Customer Churn Prediction Expert",
        goal="""
        Predict which customers are most likely to churn.
        Estimate risk level and explain why.
        """,
        backstory="""
        You are a banking churn prediction specialist.
        You analyze retrieved customer records and classify
        customers into
        • Low Risk
        • Medium Risk
        • High Risk
        You always explain the reasons behind the prediction.
        """,
        verbose=False,
        llm=llm
    )