import os
import time
import re
import litellm
from dotenv import load_dotenv
from crewai import LLM

# Monkey-patch litellm.completion to handle Groq Rate Limit (429) globally
original_completion = litellm.completion

def wrapped_completion(*args, **kwargs):
    max_retries = 8
    backoff = 10
    
    for attempt in range(max_retries):
        try:
            return original_completion(*args, **kwargs)
        except Exception as e:
            err_str = str(e)
            is_rate_limit = (
                "RateLimitError" in err_str 
                or "rate_limit_exceeded" in err_str 
                or "rate limit" in err_str.lower()
                or "429" in err_str
            )
            
            if is_rate_limit and attempt < max_retries - 1:
                match = re.search(r"try again in (\d+\.?\d*)s", err_str)
                wait_seconds = float(match.group(1)) + 2.0 if match else backoff
                print(f"\n⚠️ Groq Rate Limit Hit globally! Sleeping {wait_seconds:.2f} seconds before retrying API call (attempt {attempt+1}/{max_retries})...", flush=True)
                time.sleep(wait_seconds)
                backoff *= 1.5
            else:
                raise e

litellm.completion = wrapped_completion

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
                max_retries=12,
                timeout=120,
            )
    else:
        # Use Groq with smaller model
        llm = LLM(
            model="groq/llama-3.1-8b-instant",
            api_key=os.getenv("GROQ_API_KEY"),
            temperature=0.1,
            max_retries=12,
            timeout=120,
        )
        print("Using Groq (llama-3.1-8b-instant) - Note: Has rate limits (6000 TPM)")