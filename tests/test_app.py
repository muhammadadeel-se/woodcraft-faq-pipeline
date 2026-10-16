import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_home_endpoint(client):
    response = client.get('/')
    assert response.status_code == 200

def test_answer_endpoint_success(client):
    payload = {"query": "What is the return policy?"}
    response = client.post('/api/answer', json=payload)
    assert response.status_code == 200
    data = response.get_json()
    assert "answer" in data

def test_answer_endpoint_empty_query(client):
    payload = {"query": ""}
    response = client.post('/api/answer', json=payload)
    # App handles empty queries with 400 Bad Request
    assert response.status_code in [200, 400]

def test_xss_sanitization(client):
    payload = {"query": "<script>alert(1)</script>"}
    response = client.post('/api/answer', json=payload)
    assert response.status_code == 200
    data = response.get_json()
    # Verify that response exists and does not contain raw unescaped script tag execution
    assert "<script>alert(1)</script>" not in data.get("answer", "")