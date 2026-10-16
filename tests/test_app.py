import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_home_endpoint(client):
    """Test GET request to home/index endpoint."""
    response = client.get('/')
    assert response.status_code == 200

def test_answer_endpoint_success(client):
    """Test valid query to /api/answer."""
    payload = {"query": "What is the return policy?"}
    response = client.post('/api/answer', json=payload)
    assert response.status_code == 200
    data = response.get_json()
    assert "answer" in data

def test_answer_endpoint_empty_query(client):
    """Test empty query string payload."""
    payload = {"query": ""}
    response = client.post('/api/answer', json=payload)
    assert response.status_code in [200, 400]

def test_answer_endpoint_missing_json(client):
    """Test request without JSON body or missing query field."""
    response = client.post('/api/answer', data="not json", content_type="text/plain")
    assert response.status_code in [400, 415, 500]

def test_answer_endpoint_invalid_payload(client):
    """Test JSON payload missing the query key."""
    payload = {"wrong_key": "test"}
    response = client.post('/api/answer', json=payload)
    assert response.status_code in [200, 400]

def test_method_not_allowed(client):
    """Test invalid HTTP method on /api/answer."""
    response = client.get('/api/answer')
    assert response.status_code == 405

def test_xss_sanitization(client):
    """Test XSS script injection payload sanitization."""
    payload = {"query": "<script>alert(1)</script>"}
    response = client.post('/api/answer', json=payload)
    assert response.status_code == 200
    data = response.get_json()
    assert "<script>alert(1)</script>" not in data.get("answer", "")