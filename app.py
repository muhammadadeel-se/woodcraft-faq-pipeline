import os
from flask import Flask, render_template, request, jsonify
from markupsafe import escape

app = Flask(__name__)

# 1. Root Route - Browser kholte hi chat page dikhane ke liye
@app.route('/', methods=['GET'])
def home():
    return render_template('chat.html')

# 2. Chat / Ask Endpoint - RAG Query ke liye
@app.route('/ask', methods=['POST'])
def ask():
    try:
        data = request.get_json(silent=True) or {}
        user_query = data.get('query', '')
        
        # XSS Sanitization
        clean_query = escape(user_query)
        
        if not clean_query:
            return jsonify({'error': 'Empty query provided'}), 400
            
        # TODO: Aapka FAISS / RAG search pipeline response yahan return hoga
        response_text = f"Received query: {clean_query}"
        
        return jsonify({'answer': response_text})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)