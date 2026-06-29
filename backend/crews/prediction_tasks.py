from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from crewai import Task
from backend.agents.churn_prediction_agent import churn_prediction_agent

def create_prediction_task(analysis_task):
    return Task(
        description="""
        Using the churn analysis from the prior task, predict customer churn risk.

        Categorize customers into:
        - Low Risk
        - Medium Risk
        - High Risk

        For each category provide:
        - supporting evidence from the analysis
        - key churn factors
        - confidence score (0-100%)

        Do not invent customers not present in the analysis context.
        """,
        expected_output="""
        Prediction report with risk categories, evidence, and confidence score.
        """,
        agent=churn_prediction_agent,
        context=[analysis_task],
    )