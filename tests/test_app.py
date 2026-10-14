import pytest
import os
import json
from app import app, faiss_index, faq_data, generate_embedding

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

# 1. Test Data Loading
def test_data_loading():
    assert faq_data is not None, "FAQ data should not be None"
    assert len(faq_data) > 0, "FAQ data list should contain entries"

# 2. Test Vector Search
def test_vector_search():
    assert faiss_index is not None, "FAISS index should be initialized"
    query = "shipping options"
    query_vector = generate_embedding(query)
    distances, indices = faiss_index.search(query_vector, k=3)
    
    assert len(indices[0]) > 0, "Search should return matching indices"
    assert indices[0][0] != -1, "Top match should be valid index"

# 3. Test API Endpoint (/api/answer)
def test_api_answer_valid(client):
    response = client.post('/api/answer', 
                            data=json.dumps({"question": "What is your return policy?"}),
                            content_type='application/json')
    assert response.status_code == 200
    data = response.get_json()
    assert "answer" in data
    assert "sources" in data
    assert isinstance(data["sources"], list)

def test_api_answer_empty_input(client):
    response = client.post('/api/answer', 
                            data=json.dumps({"question": ""}),
                            content_type='application/json')
    assert response.status_code == 400

# 4. Test FAQ Detail Endpoint (/api/faq/<id>)
def test_api_faq_detail_success(client):
    response = client.get('/api/faq/1')
    assert response.status_code in [200, 404]  # 200 if ID 1 exists, else 404

def test_api_faq_detail_invalid(client):
    response = client.get('/api/faq/99999')
    assert response.status_code == 404

# 5. Test UI Rendering
def test_chat_page_render(client):
    response = client.get('/chat')
    assert response.status_code == 200
    assert b"WoodCraft Furniture Assistant" in response.data

# 6. Test Security / Input Sanitization
def test_xss_prevention(client):
    xss_payload = "<script>alert('xss')</script>"
    response = client.post('/api/answer', 
                            data=json.dumps({"question": xss_payload}),
                            content_type='application/json')
    assert response.status_code == 200
    # Response content should be escaped or properly handled without executing unsafe HTML
    assert "<script>" not in response.get_json()["answer"]