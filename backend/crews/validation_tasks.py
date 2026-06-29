from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from crewai import Task
from backend.agents.validation_agent import validation_agent


def create_validation_task(
    recommendation_task,
    query_task,
    analysis_task,
):
    return Task(
        description="""
        Validate the generated recommendations against all prior outputs.

        Use the Grounding Validation Tool on the recommendation text.
        Cross-check recommendations against:
        - retrieved customer records (query task)
        - churn analysis (analysis task)
        - predictions and recommendations (recommendation task)

        Flag hallucinations, unsupported claims, and low-confidence outputs.
        If confidence is below 70%, state "Insufficient Evidence".
        """,
        expected_output="""
        Validation summary with evidence checks, confidence score,
        and any flagged issues.
        """,
        agent=validation_agent,
        context=[recommendation_task, query_task, analysis_task],
    )
