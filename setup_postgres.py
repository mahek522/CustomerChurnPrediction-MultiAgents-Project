"""
Setup script to initialize PostgreSQL database.
"""
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[0]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from backend.memory.init_db import initialize_database


def main():
    """Main setup function."""
    print("=" * 60)
    print("PostgreSQL Database Setup")
    print("=" * 60)
    print()
    
    print("Initializing database tables...")
    try:
        initialize_database()
        print("\n" + "=" * 60)
        print("PostgreSQL Database Setup Complete! ✓")
        print("=" * 60)
        print()
        print("Database tables created:")
        print("  - memory_records")
        print("  - user_sessions")
        print("  - conversation_history")
        print("  - generated_reports")
        print("  - agent_memory")
        print()
    except Exception as e:
        print(f"\n✗ Error initializing database: {e}")
        print()
        print("Make sure PostgreSQL is running and the connection string in")
        print("backend/services/config.py is correct.")
        print()


if __name__ == "__main__":
    main()
