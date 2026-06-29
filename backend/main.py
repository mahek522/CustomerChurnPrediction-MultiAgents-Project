"""
Main entry point for the Customer Churn Intelligence Platform.
"""
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from backend.crews.churn_crew import execute_churn_crew


def main():
    """
    Main function to run the churn prediction crew.
    """
    print("=" * 70)
    print("Customer Churn Intelligence Platform")
    print("=" * 70)
    print()
    
    session_id = input("Enter session ID (or press Enter for default): ").strip()
    if not session_id:
        session_id = "session_001"
    
    user_query = input("Enter your query: ").strip()
    if not user_query:
        user_query = "Which customers are likely to churn?"
    
    context = input("Enter additional context (optional): ").strip()
    
    print()
    print("Processing your query...")
    print()
    
    result = execute_churn_crew(
        session_id=session_id,
        user_query=user_query,
        context=context,
    )
    
    print()
    print("=" * 70)
    print("RESULT")
    print("=" * 70)
    print(result)
    print("=" * 70)


if __name__ == "__main__":
    main()
