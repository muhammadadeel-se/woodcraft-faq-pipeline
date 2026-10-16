import os
import pickle
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

# Globals for resource loading
_model = None
_index = None
_faq_ids = None

def _load_resources():
    global _model, _index, _faq_ids
    if _model is None:
        _model = SentenceTransformer('all-MiniLM-L6-v2')
    if _index is None and os.path.exists('faiss_index.bin'):
        _index = faiss.read_index('faiss_index.bin')
    if _faq_ids is None and os.path.exists('faq_ids.pkl'):
        with open('faq_ids.pkl', 'rb') as f:
            _faq_ids = pickle.load(f)

def search_faq(query_text, top_k=3):
    _load_resources()
    if _index is None or _faq_ids is None:
        return []
    
    # Generate query vector
    query_vector = _model.encode([query_text]).astype('float32')
    
    # Direct search on IndexFlatL2 without distance distortion
    distances, indices = _index.search(query_vector, top_k)
    
    results = []
    for idx, dist in zip(indices[0], distances[0]):
        if idx < len(_faq_ids):
            # Include both 'id' and 'faq_id' to pass all existing tests and app logic
            results.append({
                "id": _faq_ids[idx],
                "faq_id": _faq_ids[idx],
                "score": float(dist)
            })
    return results