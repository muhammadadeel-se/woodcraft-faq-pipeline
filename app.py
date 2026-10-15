import os
import json
import numpy as np
from flask import Flask, render_template, request, jsonify
from markupsafe import escape
from sentence_transformers import SentenceTransformer
import faiss

app = Flask(__name__)

# 1. Load Embedding Model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Helper function expected by tests
def generate_embedding(text):
    return model.encode([text]).astype('float32')

# Load or create FAISS index
index_file = 'faiss_index.bin'
if os.path.exists(index_file):
    faiss_index = faiss.read_index(index_file)
else:
    # Default 384 dimensions for all-MiniLM-L6-v2
    faiss_index = faiss.IndexFlatL2(384)

# Load FAQ data
faq_data = []
if os.path.exists('faq.json'):
    with open('faq.json', 'r') as f:
        faq_data = json.load(f)

# ----------------- ROUTES ----------------- #

@app.route('/', methods=['GET'])
@app.route('/chat', methods=['GET'])
def chat():
    return render_template('chat.html')

@app.route('/api/faq', methods=['GET'])
def get_faq():
    return jsonify({'faqs': faq_data}), 200

@app.route('/api/answer', methods=['POST'])
@app.route('/ask', methods=['POST'])
def answer():
    try:
        data = request.get_json(silent=True) or {}
        user_query = data.get('query', '')
        
        # XSS Sanitization
        clean_query = escape(user_query)
        
        if not clean_query:
            return jsonify({'error': 'Empty query provided'}), 400
            
        # Vector Search
        query_vector = generate_embedding(clean_query)
        k = 1
        
        if faiss_index.ntotal > 0:
            distances, indices = faiss_index.search(query_vector, k)
            idx = indices[0][0]
            if faq_data and 0 <= idx < len(faq_data):
                ans = faq_data[idx].get('answer', "I couldn't find an exact answer in our FAQ.")
            else:
                ans = f"Query received: {clean_query}"
        else:
            ans = f"Query received: {clean_query}"
            
        return jsonify({'answer': ans}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)