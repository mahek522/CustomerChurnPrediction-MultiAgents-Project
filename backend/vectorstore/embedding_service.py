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
        
    # 2. Try HuggingFace Serverless Inference API in batches of 50
    import time
    batch_size = 50
    all_embeddings = []
    
    try:
        print(f"Generating embeddings for {len(texts)} texts via HuggingFace Inference API in batches of {batch_size}...")
        api_url = "https://api-inference.huggingface.co/models/sentence-transformers/all-MiniLM-L6-v2"
        headers = {}
        
        # Use token if available
        hf_token = os.getenv("HF_TOKEN")
        if hf_token:
            headers["Authorization"] = f"Bearer {hf_token}"
            
        for i in range(0, len(texts), batch_size):
            batch_texts = texts[i:i+batch_size]
            batch_success = False
            batch_result = None
            
            # Retry mechanism for transient DNS/connection issues
            for attempt in range(3):
                try:
                    response = requests.post(
                        api_url,
                        headers=headers,
                        json={"inputs": batch_texts, "options": {"wait_for_model": True}},
                        timeout=30
                    )
                    if response.status_code == 200:
                        batch_result = response.json()
                        if isinstance(batch_result, list) and len(batch_result) > 0:
                            # Handle single text input returning flat list vs list of lists
                            if isinstance(batch_result[0], list):
                                all_embeddings.extend(batch_result)
                            elif isinstance(batch_result[0], float):
                                all_embeddings.append(batch_result)
                            batch_success = True
                            break
                    print(f"Batch {i//batch_size + 1} attempt {attempt + 1} returned status {response.status_code}. Retrying...")
                except Exception as e:
                    print(f"Batch {i//batch_size + 1} attempt {attempt + 1} failed: {e}. Retrying...")
                time.sleep(2) # Short delay before retry
                
            if not batch_success:
                raise RuntimeError(f"Failed to generate embeddings for batch starting at index {i}")
                
        if len(all_embeddings) == len(texts):
            return all_embeddings
            
        print("Mismatched embedding count. Falling back to local SentenceTransformer.")
    except Exception as api_err:
        print(f"HuggingFace API process failed: {api_err}. Falling back to local SentenceTransformer.")

    # 3. Fallback to local SentenceTransformer (Disabled on Render to avoid OOM)
    if os.getenv("RENDER") is not None:
        raise RuntimeError(
            "Embedding generation failed: HuggingFace Inference API was unavailable, "
            "and local SentenceTransformer loading is disabled on Render to prevent OOM crashes."
        )

    model = get_model()
    if model is None:
        raise RuntimeError("Embedding model not loaded")
    try:
        embeddings = model.encode(texts, show_progress_bar=False)
        return embeddings.tolist()
    except Exception as e:
        print(f"Error generating embeddings: {e}")
        raise