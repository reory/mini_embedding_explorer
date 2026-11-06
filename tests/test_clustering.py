import numpy as np

from embeddings import cluster_points


def test_cluster_points_returns_a_label_per_point():
    """Ensure one cluster label is returned for each input point."""

    # Two groups of points.
    points = np.array([
        [0.0, 0.0],
        [0.1, 0.1],
        [5.0, 5.0],
        [5.1, 5.1],
    ])

    labels = cluster_points(points, n_clusters=2)

    # Every point should receive a cluster assignment.
    assert len(labels) == len(points)


def test_cluster_points_returns_expected_number_of_clusters():
    """Ensure KMeans creates the requested number of clusters."""

    # Three clearly separated groups.
    points = np.array([
        [0.0, 0.0],
        [0.1, 0.1],
        [5.0, 5.0],
        [5.1, 5.1],
        [10.0, 10.0],
        [10.1, 10.1],
    ])

    labels = cluster_points(points, n_clusters=3)

    # Confirm the requested cluster count was created.
    assert len(set(labels)) == 3


def test_cluster_points_returns_integer_labels():
    """Ensure cluster labels are integers."""

    points = np.array([
        [0.0, 0.0],
        [1.0, 1.0],
        [2.0, 2.0],
        [3.0, 3.0],
    ])

    labels = cluster_points(points, n_clusters=2)

    # KMeans should return integer-based cluster identifiers.
    assert all(isinstance(label, (int, np.integer)) for label in labels)