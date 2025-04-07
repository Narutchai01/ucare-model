import pytest
from unittest.mock import patch

@pytest.fixture
def mock_sentence_transformer():
    with patch('sentence_transformers.SentenceTransformer') as mock:
        yield mock

def test_get_skincare_recommendations(mock_sentence_transformer):
    from skincare_recommand import get_skincare_recommendations
    mock_sentence_transformer.return_value = mock_sentence_transformer
    recommendations = get_skincare_recommendations("dry skin")
    assert recommendations is not None
    assert isinstance(recommendations, list)