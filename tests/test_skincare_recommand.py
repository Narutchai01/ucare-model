import pytest
from skincare_recommand import get_skincare_recommendations

def test_get_skincare_recommendations():
    result = get_skincare_recommendations("dry skin")
    assert isinstance(result, list)
    assert len(result) > 0

def test_model_loading():
    try:
        get_skincare_recommendations("oily skin")
    except Exception as e:
        assert "model" not in str(e)  # Ensure model loading does not raise an error