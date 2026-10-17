import pytest
from unittest.mock import patch
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_home_endpoint(client):
    """Test GET request to the home index page."""
    response = client.get('/')
    assert response.status_code == 200

def test_answer_endpoint_success(client):
    """Test successful FAQ query submission."""
    payload = {"query": "What is the return policy for custom furniture?"}
    response = client.post('/api/answer', json=payload)
    assert response.status_code == 200
    data = response.get_json()
    assert "answer" in data

def test_answer_endpoint_empty_query(client):
    """Test submission with an empty query string."""
    payload = {"query": ""}
    response = client.post('/api/answer', json=payload)
    assert response.status_code in [200, 400]

def test_answer_endpoint_missing_json(client):
    """Test request with non-JSON or missing body."""
    response = client.post('/api/answer', data="plain text", content_type="text/plain")
    assert response.status_code in [400, 415, 500]

def test_answer_endpoint_missing_query_key(client):
    """Test JSON payload missing the 'query' key."""
    payload = {"question": "Missing query key"}
    response = client.post('/api/answer', json=payload)
    assert response.status_code in [200, 400]

def test_answer_endpoint_exception_handling(client):
    """Test exception handling branch inside /api/answer."""
    with patch('search.search_faq', side_effect=Exception("Database or Search Error")):
        payload = {"query": "Test exception"}
        response = client.post('/api/answer', json=payload)
        assert response.status_code in [200, 500]
        data = response.get_json()
        assert data is not None

def test_method_not_allowed(client):
    """Test unsupported HTTP method on API endpoint."""
    response = client.get('/api/answer')
    assert response.status_code == 405

def test_xss_sanitization(client):
    """Test XSS script injection sanitization."""
    payload = {"query": "<script>alert('xss')</script>"}
    response = client.post('/api/answer', json=payload)
    assert response.status_code == 200
    data = response.get_json()
    assert "<script>" not in data.get("answer", "")