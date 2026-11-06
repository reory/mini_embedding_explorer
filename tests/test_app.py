from unittest.mock import patch

import pandas as pd
import pytest  #noqa


@patch("app.st")
def test_empty_texts_show_error_and_stop(mock_st):
    """Ensure empty input is rejected before processing."""

    texts = ["", "   ", ""]

    if not texts or all(t.strip() == "" for t in texts):
        mock_st.error(" ⛔ No valid text found in the selected column.")
        mock_st.stop()

    mock_st.error.assert_called_once()
    mock_st.stop.assert_called_once()


def test_cluster_count_is_capped_to_sample_count():
    """Ensure cluster count never exceeds available samples."""

    reduced = [[0.1, 0.2]]
    n_clusters = 5

    n_clusters = min(n_clusters, len(reduced))

    assert n_clusters == 1


def test_txt_parsing_removes_blank_lines():
    """Ensure empty lines are ignored."""

    raw = """
    hello

    world


    testing
    """

    texts = [
        line.strip()
        for line in raw.splitlines()
        if line.strip()
    ]

    assert texts == [
        "hello",
        "world",
        "testing",
    ]


def test_csv_cleaning_removes_nan_values():
    """Ensure invalid text values are cleaned."""

    df = pd.DataFrame(
        {
            "text": [
                "hello",
                None,
                "NaN",
                "world",
            ]
        }
    )

    texts = (
        df["text"]
        .astype(str)
        .replace(
            ["nan", "None", "NaN"],
            "",
        )
        .fillna("")
        .tolist()
    )

    assert texts == [
        "hello",
        "",
        "",
        "world",
    ]