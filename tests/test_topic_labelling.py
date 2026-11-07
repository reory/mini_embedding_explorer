from topic_labelling import (
    clean_words,
    extract_keywords,
    generate_cluster_labels,
)


def test_clean_words_removes_stopwords():
    """Common stopwords should be removed."""

    result = clean_words(
        "The delivery was late and the package arrived"
    )

    assert result == [
        "delivery",
        "late",
        "package",
        "arrived",
    ]


def test_extract_keywords_returns_most_common_words():
    """Most frequent words should be returned first."""

    texts = [
        "delivery delivery tracking",
        "delivery arrived",
    ]

    result = extract_keywords(texts, top_n=2)

    assert result == [
        "delivery",
        "tracking",
    ]


def test_generate_cluster_labels_creates_label_per_cluster():
    """Each cluster should receive a generated label."""

    texts = [
        "delivery arrived late",
        "package delivery delayed",
        "website login failed",
        "password reset broken",
    ]

    labels = [0, 0, 1, 1]

    result = generate_cluster_labels(
        texts,
        labels,
    )

    assert 0 in result
    assert 1 in result


def test_generate_cluster_labels_returns_expected_cluster_count():
    """Return one label for each cluster."""

    texts = [
        "delivery late",
        "website login",
        "refund request",
    ]

    labels = [0, 1, 2]

    result = generate_cluster_labels(
        texts,
        labels,
    )

    assert len(result) == 3


def test_generate_cluster_labels_uses_fallback_for_empty_cluster():
    """Fallback label should be used when no keywords exist."""

    texts = ["a an the"]
    labels = [0]

    result = generate_cluster_labels(
        texts,
        labels,
    )

    assert result[0] == "Cluster0"


def test_generate_cluster_labels_title_cases_keywords():
    """Generated labels should be title cased."""

    texts = [
        "delivery tracking",
        "delivery arrived",
    ]

    labels = [0, 0]

    result = generate_cluster_labels(
        texts,
        labels,
    )

    assert "Delivery" in result[0]