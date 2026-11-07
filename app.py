# Streamlit UI

# # [PORTFOLIO_PROJECT] Mini Embedding Explorer.
# [PORTFOLIO_CHALLENGE] App kept crashing eventhough code was running ok.
# [PORTFOLIO_DESCRIPTION] App kept crashing for unknown reason.
# [PORTFOLIO_SOLUTION] Generated a saftey check to prevent app from crashing.

# Upload CSV or TXT → Select column → Generate Embeddings → Visualise

import pandas as pd
import streamlit as st

from embeddings import cluster_points, generate_embeddings, reduce_dimensions
from topic_labelling import generate_cluster_labels

st.set_page_config(
    page_title="Mini Embedding Explorer", 
    layout="wide", 
    page_icon="📊"
)

# Header
st.title("📊 Mini Embedding Explorer")
st.caption(
    "Upload text data -> generate embeddings -> "
    "visualise clusters -> discover insights."
)

st.markdown("---")

# Sidebar section heading
st.sidebar.header("⚙️ Settings")

model_name = st.sidebar.selectbox(
    "Embedding Model", 
    ["sentence-transformers/all-MiniLM-L6-v2"],
    help=(
        "The AI model used to convert text into embeddings. "
        "Different models may produce different clustering results."
    ),
)

reduction_method = st.sidebar.selectbox(
    "Dimensionality Reduction", 
    ["PCA (fast)", "UMAP (high quality)"],
    help=(
        "Converts high-dimensional embeddings into a 2D visualisation. "
        "PCA is faster, while UMAP may produce clearer cluster separation."
    ),
)

n_clusters = st.sidebar.slider(
    "Number of Clusters", 
    min_value=2, 
    max_value=12, 
    value=5,
    help=(
        "Controls how many groups the data is split into. "
        "Lower values create broader themes, while higher values "
        "create more detailed and specific groups. "
        "If keyword labels appear too generic, try increasing the cluster count."
    ),
)

st.sidebar.markdown("---")
st.sidebar.info(
    "Tip: Use CSV for large datasets. TXT is fine for simple lists."
)

# Store extracted text records.
texts = []

# File Upload
uploaded_file = st.file_uploader("Upload CSV or TXT", type=["csv", "txt"])

if uploaded_file is not None:
    # Load data
    if uploaded_file.name.endswith(".csv"):
        df = pd.read_csv(
            uploaded_file,
            encoding="utf-8",
            encoding_errors="ignore",
            on_bad_lines="skip",
        )
        # Drop completly empty rows
        df = df.dropna(how="all")

        st.subheader("📖 Data Preview")
        st.caption("Preview the uploaded dataset before generating embeddings.")
        st.dataframe(df.head())

        # Select columns before dropping rows
        text_column = st.selectbox("Select text column", df.columns)

        # Drop rows where the selected column is missing
        df = df.dropna(subset=[text_column])

        # Force everything to clean strings
        texts = (
            df[text_column]
            .astype(str)
            .replace(["nan", "None", "NaN"], "")
            .fillna("")
            .tolist()
        )
    else:
        raw = uploaded_file.read().decode("utf-8")
        texts = [line.strip() for line in raw.splitlines() if line.strip()]

        st.subheader("📖 Loaded Text")
        st.write(texts[:10])

# Generate Embeddings Tool
# Saftey check to prevent the app from crashing
if st.button("🚀 Generate Embeddings"):

    if not uploaded_file:
        st.error("⛔ Please upload a CSV or TXT file first.")
        st.stop()

    if not texts or all(t.strip() == "" for t in texts):
        st.error(" ⛔ No valid text found in the selected column.")
        st.stop()

    with st.spinner("Generate Embeddings.."):
        vectors = generate_embeddings(texts, model_name)

    with st.spinner("Reducing Dimensions.."):
        reduced = reduce_dimensions(vectors, method=reduction_method)

    # Ensure cluster count does not exceed number of samples (safety check)
    if len(reduced) < n_clusters:
        st.warning(
            f" Not enough samples ({len(reduced)}) for {n_clusters} clusters."
            f"Adjusting to {len(reduced)}."
        )
        n_clusters = len(reduced)

    with st.spinner("Clustering points.."):
        labels = cluster_points(reduced, n_clusters=n_clusters)

    st.success("✅ Embeddings Generated Successfully!")

    # Visualisations
    st.subheader("✅ 2D Embedding Visualisation")
    st.caption(
        "Each point represents a text record. Similar records appear closer together "
        "and are grouped into clusters. The x and y values are automatically generated " 
        "and have no direct meaning."
    )
    plot_df = pd.DataFrame(
        {
            "x": reduced[:, 0],
            "y": reduced[:, 1],
            "cluster": labels,
            "text": texts,
        }
    )

    st.scatter_chart(plot_df, x="x", y="y", color="cluster")

    # Generate human-readable topic labels.
    topic_labels = generate_cluster_labels(
        texts,
        labels,
    )

    # Topic Overview
    st.subheader(" 🏷️ Cluster Keywords")
    st.caption(
        "Keywords are generated from the most common terms "
        "found within each cluster."
    )

    topic_df = pd.DataFrame(
        [
            {"cluster": cluster, "keywords": topic}
            for cluster, topic in topic_labels.items()
        ]
    )

    st.dataframe(topic_df)

    # Cluster Summary
    st.subheader("📊 Cluster Summary")
    st.caption(
        "Use the cluster and keyword columns to understand "
        "how related pieces of text have been grouped together."
    )
    plot_df["topic"] = plot_df["cluster"].map(topic_labels)
    summary_df = plot_df[
        ["text", "cluster", "topic"]
    ]
    st.dataframe(summary_df)

    # Download Results
    csv = summary_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="Download Clustered Data",
        data=csv,
        file_name="clustered_text.csv",
        mime="text/csv",
    )
