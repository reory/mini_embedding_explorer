import numpy as np
from hypothesis import HealthCheck, assume, given, settings
from hypothesis.extra.numpy import arrays

from embeddings import reduce_dimensions


@settings(suppress_health_check=[HealthCheck.too_slow])
@given(
    arrays(
        dtype=np.float64,
        shape=(10, 5),
        elements={"min_value": -100, "max_value": 100},
    )
)
def test_pca_preserves_row_count(vectors):
    """PCA should never change the number of rows."""

    # Skip constant matrices that have zero variance and trigger
    # sklearn PCA runtime warnings.
    assume(np.var(vectors) > 0)

    reduced = reduce_dimensions(vectors, method="PCA (fast)")

    assert reduced.shape[0] == vectors.shape[0]


@settings(suppress_health_check=[HealthCheck.too_slow])
@given(
    arrays(
        dtype=np.float64,
        shape=(10, 5),
        elements={"min_value": -100, "max_value": 100},
    )
)
def test_pca_returns_two_dimensions(vectors):
    """PCA should return two columns by default."""

    assume(np.var(vectors) > 0)

    reduced = reduce_dimensions(vectors, method="PCA (fast)")

    assert reduced.shape[1] == 2


@settings(suppress_health_check=[HealthCheck.too_slow])
@given(
    arrays(
        dtype=np.float64,
        shape=(20, 8),
        elements={"min_value": -100, "max_value": 100},
    )
)
def test_pca_output_contains_no_nan_values(vectors):
    """PCA output should not contain NaN values."""

    assume(np.var(vectors) > 0)

    reduced = reduce_dimensions(vectors, method="PCA (fast)")

    assert not np.isnan(reduced).any()