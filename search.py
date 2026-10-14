import os
import pickle
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

MODEL_NAME = "all-MiniLM-L6-v2"
_model = None
_index = None
_faq_ids = None

def _load_resources():
    global _model, _index, _faq_ids
    if _model is None:
        _model = SentenceTransformer(MODEL_NAME)
    if _index is None:
        if not os.path.exists("faiss_index.bin") or not os.path.exists("faq_ids.pkl"):
            raise FileNotFoundError("FAISS index or ID mapping not found. Run build_index.py first.")
        _index = faiss.read_index("faiss_index.bin")
    if _faq_ids is None:
        with open("faq_ids.pkl", "rb") as f:
            _faq_ids = pickle.load(f)

def search_faq(query: str, top_k: int = 3):
    _load_resources()
    query_vector = _model.encode([query]).astype("float32")
    faiss.normalize_L2(query_vector)
    
    distances, indices = _index.search(query_vector, top_k)
    
    results = []
    for idx, score in zip(indices[0], distances[0]):
        if idx != -1:
            results.append({
                "faq_id": int(_faq_ids[idx]),
                "score": float(score)
            })
    return results