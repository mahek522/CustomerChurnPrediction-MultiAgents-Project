from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from crewai import Task
from backend.agents.recommendation_agent import recommendation_agent

def create_recommendation_task(prediction_task):
    return Task(
        description="""
        Using the churn predictions from the prior task, generate personalized
        retention strategies for high-risk and medium-risk customers.

        Include:
        - specific retention actions
        - priority (High/Medium/Low)
        - expected business impact
        - evidence linking each recommendation to customer data
        """,
        expected_output="""
        Retention recommendations with priority and expected impact.
        """,
        agent=recommendation_agent,
        context=[prediction_task],
    )