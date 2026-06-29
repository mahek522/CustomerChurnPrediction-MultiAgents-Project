# Troubleshooting Guide

## Rate Limit Issues

### Problem: Groq API Rate Limit (429 Error)

**Error Message:**
```
RateLimitError: Rate limit reached for model `llama-3.1-8b-instant` 
Limit 6000 TPM, Used 4648, Requested 4451
```

**Cause:**
Groq's free on-demand tier has a limit of 6000 tokens per minute (TPM). The multi-agent system makes multiple LLM calls, which can exceed this limit.

### Solutions

#### Solution 1: Wait for Rate Limit Reset (Quickest)
- Wait 30-60 seconds for the rate limit to reset
- Run the test again
- This is temporary and will happen again

#### Solution 2: Install Ollama (Recommended - Permanent Fix)

Ollama runs LLMs locally with no rate limits and is completely free.

**Installation:**
1. Download Ollama from https://ollama.com/download
2. Install it on your system
3. Pull the model:
   ```bash
   ollama pull llama3.2
   ```
4. Update `.env` file:
   ```env
   USE_OLLAMA=true
   ```
5. Run your test

**Benefits:**
- No rate limits
- Free usage
- Data stays on your machine (privacy)
- Faster execution (no network latency)

See [OLLAMA_SETUP.md](OLLAMA_SETUP.md) for detailed instructions.

#### Solution 3: Upgrade to Groq Dev Tier

Groq offers a Dev Tier with higher rate limits.

1. Go to https://console.groq.com/settings/billing
2. Upgrade to Dev Tier
3. Your rate limits will increase significantly

#### Solution 4: Reduce Token Usage

If you must use Groq free tier:

1. **Use smaller prompts** - Reduce context passed to agents
2. **Increase delays** - Add longer delays between agent executions
3. **Run fewer agents** - Simplify the workflow
4. **Use smaller model** - Already using `llama-3.1-8b-instant`

### Current Configuration

The system is configured to:
- Use Groq `llama-3.1-8b-instant` by default
- Retry up to 5 times with exponential backoff
- Add delays between tasks when using Groq

### Testing After Rate Limit Reset

After waiting for the rate limit to reset:

```bash
# Test the crew
.venv\Scripts\python.exe -m backend.crews.test_crew
```

If you still hit rate limits, consider installing Ollama.

## Other Common Issues

### Issue: Ollama Connection Refused

**Error:**
```
OllamaException - [WinError 10061] No connection could be made 
because the target machine actively refused it
```

**Solution:**
1. Ensure Ollama is installed and running
2. Check if Ollama service is started
3. Verify Ollama is running on `http://localhost:11434`
4. If using a different port, update `backend/agents/llm_config.py`

### Issue: PostgreSQL Connection Failed

**Error:**
```
OperationalError: could not connect to server
```

**Solution:**
1. Ensure PostgreSQL is running
2. Verify connection string in `backend/services/config.py`
3. Create the database:
   ```bash
   createdb churn_memory_db
   ```
4. Run initialization:
   ```bash
   python setup_postgres.py
   ```

### Issue: ChromaDB Collection Not Found

**Error:**
```
ValueError: Collection 'customer_documents' not found
```

**Solution:**
1. Initialize ChromaDB with customer data:
   ```bash
   python setup_chromadb.py
   ```
2. Verify the dataset exists at `datasets/BNPParibas_Data.csv`

### Issue: Import Errors

**Error:**
```
ModuleNotFoundError: No module named 'backend.xxx'
```

**Solution:**
1. Ensure you're in the project root directory
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Check that the file exists in the correct location

### Issue: Empty Files or Folders

If you encounter empty files or folders:

1. **Empty policy files** - These have been populated with content
2. **Empty `backend/main.py`** - This has been populated
3. **Empty `backend/__init__.py`** - This has been populated
4. **Empty `tests/` folder** - Contains `test_api.py` for testing

## Getting Help

If you encounter issues not covered here:

1. Check the [README.md](README.md) for setup instructions
2. Review the [OLLAMA_SETUP.md](OLLAMA_SETUP.md) for Ollama configuration
3. Check the policy files in `policies/` for business rules
4. Review agent configurations in `backend/agents/`

## Best Practices

### For Development
- Use Ollama for local development (no rate limits)
- Test with smaller datasets first
- Monitor token usage in Groq console

### For Production
- Upgrade to Groq Dev Tier or Enterprise
- Implement proper error handling
- Add monitoring and alerting
- Use load balancing for high traffic

### For Testing
- Use mock data when possible
- Test individual components before full workflow
- Keep test queries simple
- Monitor rate limit usage
