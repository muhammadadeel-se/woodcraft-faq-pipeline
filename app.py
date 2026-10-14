import os
import pickle
import numpy as np
from flask import Flask, render_template, request, jsonify
from markupsafe import escape
from sentence_transformers import SentenceTransformer
import faiss

app = Flask(__name__)

# 1. Load Embedding Model & FAISS Index once at startup
print("Loading model and FAISS index...")
model = SentenceTransformer('all-MiniLM-L6-v2')

# Load index and metadata (faiss_index.bin and faq_ids.pkl or faq.json)
index = faiss.read_index('faiss_index.bin')

# Load FAQ data mapping if available
faq_data = []
if os.path.exists('faq.json'):
    import json
    with open('faq.json', 'r') as f:
        faq_data = json.load(f)

@app.route('/', methods=['GET'])
def home():
    return render_template('chat.html')

@app.route('/ask', methods=['POST'])
def ask():
    try:
        data = request.get_json(silent=True) or {}
        user_query = data.get('query', '')
        
        # XSS Sanitization
        clean_query = escape(user_query)
        
        if not clean_query:
            return jsonify({'error': 'Empty query provided'}), 400
            
        # Perform RAG Vector Search using FAISS
        query_vector = model.encode([clean_query]).astype('float32')
        k = 1  # Top 1 matching result
        distances, indices = index.search(query_vector, k)
        
        # Retrieve answer based on index
        idx = indices[0][0]
        if faq_data and 0 <= idx < len(faq_data):
            answer = faq_data[idx].get('answer', "I'm sorry, I couldn't find a matching answer in our FAQ.")
        else:
            answer = f"Based on our furniture catalog, we received your query about: {clean_query}. (FAISS Index match index: {idx})"
            
        return jsonify({'answer': answer})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)