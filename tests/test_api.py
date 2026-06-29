"""
Test script for FastAPI backend endpoints.
"""
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import requests
import json


def test_health():
    """Test health check endpoint."""
    try:
        response = requests.get("http://localhost:8000/health")
        print(f"Health Check: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Health check failed: {e}")
        return False


def test_query():
    """Test query endpoint."""
    try:
        payload = {
            "session_id": "test_session",
            "user_query": "Which customers are likely to churn?",
            "context": "Test query"
        }
        response = requests.post(
            "http://localhost:8000/query",
            json=payload,
            timeout=300
        )
        print(f"Query: {response.status_code}")
        if response.status_code == 200:
            print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Query test failed: {e}")
        return False


def test_history():
    """Test history endpoint."""
    try:
        response = requests.get("http://localhost:8000/history/test_session")
        print(f"History: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"History test failed: {e}")
        return False


if __name__ == "__main__":
    print("=" * 60)
    print("API Endpoint Tests")
    print("=" * 60)
    print()
    
    print("1. Testing Health Check...")
    health_ok = test_health()
    print()
    
    print("2. Testing Query Endpoint...")
    query_ok = test_query()
    print()
    
    print("3. Testing History Endpoint...")
    history_ok = test_history()
    print()
    
    print("=" * 60)
    if health_ok and query_ok and history_ok:
        print("All tests passed! ✓")
    else:
        print("Some tests failed.")
    print("=" * 60)
