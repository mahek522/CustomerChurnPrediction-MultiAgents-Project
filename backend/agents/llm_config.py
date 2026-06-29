import os
import time
from dotenv import load_dotenv
from crewai import LLM

load_dotenv(override=True)

# Check for mock mode (for testing without rate limits)
USE_MOCK_MODE = os.getenv("USE_MOCK_MODE", "false").lower() == "true"

if USE_MOCK_MODE:
    # Mock mode - doesn't call any LLM API
    print("⚠️  MOCK MODE ENABLED - No LLM calls will be made")
    print("   This is for testing workflow without rate limits")
    os.environ["OPENAI_API_KEY"] = "mock_key"
    llm = None
else:
    # Use Ollama for local LLM (no rate limits, free)
    # Fallback to Groq if Ollama is not available
    USE_OLLAMA = os.getenv("USE_OLLAMA", "true").lower() == "true"

    if USE_OLLAMA:
        try:
            # Try to use Ollama with llama3.2 (smaller, faster)
            llm = LLM(
                model="ollama/llama3.2",
                base_url="http://localhost:11434",
                temperature=0.1,
                timeout=120,
            )
            print("Using Ollama (llama3.2) - no rate limits")
        except Exception as e:
            print(f"Ollama not available: {e}")
            print("Falling back to Groq...")
            llm = LLM(
                model="groq/llama-3.1-8b-instant",
                api_key=os.getenv("GROQ_API_KEY"),
                temperature=0.1,
                max_retries=3,
                timeout=60,
            )
    else:
        # Use Groq with smaller model
        llm = LLM(
            model="groq/llama-3.1-8b-instant",
            api_key=os.getenv("GROQ_API_KEY"),
            temperature=0.1,
            max_retries=3,
            timeout=60,
        )
        print("Using Groq (llama-3.1-8b-instant) - Note: Has rate limits (6000 TPM)")