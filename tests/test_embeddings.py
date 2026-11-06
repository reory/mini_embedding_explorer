from unittest.mock import MagicMock, patch

import numpy as np
import pytest

from embeddings import generate_embeddings, reduce_dimensions


def test_reduce_dimensions_pca_returns_two_columns():
    """Ensure PCA reduction produces 2D output."""

    # Create sample embedding vectors.
    vectors = np.random.rand(10, 5)

    reduced = reduce_dimensions(vectors, method="PCA (fast)")

    # All rows should be preserved and reduced to two dimensions.
    assert reduced.shape == (10, 2)


def test_reduce_dimensions_preserves_row_count():
    """Ensure dimensionality reduction keeps all samples."""

    vectors = np.random.rand(25, 8)

    reduced = reduce_dimensions(vectors, method="PCA (fast)")

    # No input vectors should be lost during reduction.
    assert len(reduced) == len(vectors)


def test_reduce_dimensions_supports_custom_component_count():
    """Ensure PCA honours the requested component count."""

    vectors = np.random.rand(20, 10)

    reduced = reduce_dimensions(
        vectors,
        method="PCA (fast)",
        n_components=3,
    )

    assert reduced.shape == (20, 3)


def test_reduce_dimensions_invalid_method_raises_value_error():
    """Ensure unsupported methods raise a clear error."""

    vectors = np.random.rand(10, 5)

    with pytest.raises(ValueError):
        reduce_dimensions(vectors, method="not-a-real-method")


@patch("sentence_transformers.SentenceTransformer")
def test_generate_embeddings_returns_numpy_array(mock_model_class):
    """Ensure embeddings are returned as a NumPy array."""

    mock_model = MagicMock()
    mock_model.encode.return_value = [[1.0, 2.0], [3.0, 4.0]]
    mock_model_class.return_value = mock_model

    result = generate_embeddings(["hello", "world"])

    assert isinstance(result, np.ndarray)


@patch("sentence_transformers.SentenceTransformer")
def test_generate_embeddings_returns_one_embedding_per_text(mock_model_class):
    """Ensure an embedding is produced for each input string."""

    mock_model = MagicMock()
    mock_model.encode.return_value = [[1.0], [2.0], [3.0]]
    mock_model_class.return_value = mock_model

    texts = ["a", "b", "c"]

    result = generate_embeddings(texts)

    assert len(result) == len(texts)