import pytest
from search import search_faq

def test_search_shipping():
    results = search_faq("What is your standard shipping timeframe?", top_k=3)
    assert isinstance(results, list)
    assert len(results) > 0
    assert len(results) <= 3
    assert "faq_id" in results[0]
    assert "score" in results[0]

def test_search_wood_materials():
    results = search_faq("What types of wood do you use?", top_k=2)
    assert len(results) > 0
    top_result = results[0]
    assert isinstance(top_result["faq_id"], int)
    assert top_result["score"] > 0.0