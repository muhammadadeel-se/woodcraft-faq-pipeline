import json
import pytest
from app import app, faiss_index, generate_embedding

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_chat_route(client):
    response = client.get('/chat')
    assert response.status_code == 200

def test_api_faq_route(client):
    response = client.get('/api/faq')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'faqs' in data

def test_api_answer_route(client):
    response = client.post('/api/answer', 
                            data=json.dumps({'query': 'What wood do you use?'}),
                            content_type='application/json')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'answer' in data

def test_xss_protection(client):
    response = client.post('/api/answer', 
                            data=json.dumps({'query': '<script>alert("xss")</script>'}),
                            content_type='application/json')
    assert response.status_code == 200
    assert '<script>' not in response.get_data(as_text=True)

def test_faiss_and_embedding_objects():
    assert faiss_index is not None
    embedding = generate_embedding("test query")
    assert embedding is not None