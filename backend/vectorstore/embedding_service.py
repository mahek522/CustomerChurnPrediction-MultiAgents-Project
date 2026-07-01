import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

import os
import requests
import json
from backend.services.config import EMBEDDING_MODEL

_model = None

def get_model():
    global _model
    if _model is None:
        print("Lazy loading SentenceTransformer embedding model...")
        from sentence_transformers import SentenceTransformer
        try:
            _model = SentenceTransformer(EMBEDDING_MODEL)
        except Exception as e:
            print(f"Error loading embedding model: {e}")
            _model = None
    return _model


def generate_embeddings(texts):
    # 1. Mock Mode
    if os.getenv("USE_MOCK_MODE", "false").lower() == "true":
        print("Mock mode enabled: returning dummy mock embeddings...")
        return [[0.1] * 384 for _ in texts]
        
    # 2. Try HuggingFace Serverless Inference API (Free, no token required)
    try:
        print(f"Generating embeddings for {len(texts)} texts via HuggingFace Inference API...")
        api_url = "https://api-inference.huggingface.co/pipeline/feature-extraction/sentence-transformers/all-MiniLM-L6-v2"
        headers = {}
        
        # Use token if available
        hf_token = os.getenv("HF_TOKEN")
        if hf_token:
            headers["Authorization"] = f"Bearer {hf_token}"
            
        response = requests.post(
            api_url,
            headers=headers,
            json={"inputs": texts, "options": {"wait_for_model": True}},
            timeout=30
        )
        
        if response.status_code == 200:
            embeddings = response.json()
            if isinstance(embeddings, list) and len(embeddings) > 0:
                # Ensure it's a list of floats
                if isinstance(embeddings[0], list):
                    return embeddings
                elif isinstance(embeddings[0], float):
                    return [embeddings]
                    
        print(f"HuggingFace API returned status {response.status_code}. Falling back to local SentenceTransformer.")
    except Exception as api_err:
        print(f"HuggingFace API call failed: {api_err}. Falling back to local SentenceTransformer.")

    # 3. Fallback to local SentenceTransformer
    model = get_model()
    if model is None:
        raise RuntimeError("Embedding model not loaded")
    try:
        embeddings = model.encode(texts, show_progress_bar=False)
        return embeddings.tolist()
    except Exception as e:
        print(f"Error generating embeddings: {e}")
        raise