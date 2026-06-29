# Ollama Setup Guide

This guide explains how to set up Ollama for local LLM execution, which eliminates rate limits and provides free, unlimited usage.

## Why Ollama?

- **No Rate Limits**: Run LLMs locally without API rate limits
- **Free**: No API costs
- **Privacy**: Data stays on your machine
- **Fast**: Local execution with minimal latency
- **Multiple Models**: Support for various open-source models

## Installation

### Windows

1. Download Ollama from https://ollama.com/download
2. Run the installer
3. Ollama will be installed and start automatically

### macOS

```bash
brew install ollama
```

### Linux

```bash
curl -fsSL https://ollama.com/install.sh | sh
```

## Verify Installation

Open a terminal and run:

```bash
ollama --version
```

You should see the version number.

## Pull the Model

Pull the llama3.2 model (recommended for this project):

```bash
ollama pull llama3.2
```

Or for a smaller/faster model:

```bash
ollama pull llama3.2:3b
```

## Start Ollama Server

Ollama typically starts automatically. To verify:

```bash
ollama serve
```

The server runs on `http://localhost:11434` by default.

## Test Ollama

```bash
ollama run llama3.2 "Hello, how are you?"
```

## Configure the Project

The project is already configured to use Ollama by default. Check your `.env` file:

```env
USE_OLLAMA=true
```

If you want to use Groq instead:

```env
USE_OLLAMA=false
```

## Available Models

- `llama3.2` - Latest Llama 3.2 model (recommended)
- `llama3.2:3b` - Smaller, faster version
- `llama3.1` - Previous version
- `mistral` - Alternative model
- `gemma2` - Google's Gemma model

To change the model, edit `backend/agents/llm_config.py`:

```python
llm = LLM(
    model="ollama/llama3.2:3b",  # Change model here
    base_url="http://localhost:11434",
    temperature=0.1,
    timeout=120,
)
```

## Troubleshooting

### Ollama not responding

1. Check if Ollama is running:
   ```bash
   ollama list
   ```

2. Restart Ollama:
   - Windows: Restart from system tray
   - macOS/Linux: `ollama serve`

### Model not found

Pull the model:
```bash
ollama pull llama3.2
```

### Port already in use

If port 11434 is already in use, you can change it in `backend/agents/llm_config.py`:

```python
llm = LLM(
    model="ollama/llama3.2",
    base_url="http://localhost:11435",  # Change port
    temperature=0.1,
    timeout=120,
)
```

And start Ollama on the new port:
```bash
OLLAMA_HOST=0.0.0.0:11435 ollama serve
```

### Out of Memory

If you encounter memory issues:
1. Use a smaller model: `llama3.2:3b`
2. Close other applications
3. Reduce `num_ctx` (context window) in Ollama settings

## Performance Tips

1. **Use smaller models for faster execution**: `llama3.2:3b`
2. **GPU acceleration**: Ollama automatically uses GPU if available
3. **Quantization**: Ollama uses quantized models by default for efficiency

## Switching Back to Groq

If you want to use Groq API instead:

1. Set in `.env`:
   ```env
   USE_OLLAMA=false
   ```

2. Ensure you have a valid Groq API key

3. Note: Groq has rate limits (6000 TPM for on-demand tier)

## Running the Project with Ollama

Once Ollama is set up:

```bash
# Run the test
python -m backend.crews.test_crew

# Or use the delayed execution to be extra safe
python backend/test_with_ollama.py
```

The system will automatically use Ollama if `USE_OLLAMA=true` in your `.env` file.
