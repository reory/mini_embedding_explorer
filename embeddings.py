# Helper module -> Embeddings and clustering engine

import numpy as np
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA


# Generate embeddings
def generate_embeddings(texts, model_name="sentence-transformers/all-MiniLM-L6-v2"):
    """Convert a list of text strings into vector embeddings."""

    # NOTE:
    # Keep this import inside the function. Moving it to module level
    # increased import time from ~5s to ~17s and significantly slowed
    # pytest collection because sentence-transformers pulls in large ML
    # dependencies such as transformers and torch.
    from sentence_transformers import SentenceTransformer

    model = SentenceTransformer(model_name)
    embeddings = model.encode(texts, show_progress_bar=False)

    return np.array(embeddings)


# Dimensionality Reduction (PCA or UMAP)
def reduce_dimensions(vectors, method="PCA (fast)", n_components=2):
    """
    Reduce high-dimensional embeddings to 2d for visualisation.
    Compresses high-dimensional vectors into 2D so users can see patterns.
    """

    if method == "PCA (fast)":
        # Fast baseline reduction method.
        reducer = PCA(n_components=n_components)
        return reducer.fit_transform(vectors)

    elif method == "UMAP (high quality)":
        try:
            # Import lazily to avoid loading UMAP unless requested.
            import umap
        except ImportError:
            raise ImportError("UMAP is not installed. Run: pip install umap-learn")
        reducer = umap.UMAP(n_components=n_components, random_state=42)
        return reducer.fit_transform(vectors)

    else:
        # Reject unsupported reduction methods.
        raise ValueError("Unknown reduction method.")


# Clustering KMeans
def cluster_points(points, n_clusters=5):
    """
    Cluster 2d points into groups using KMeans.
    Groups similar texts together —
    perfect for customer feedback, HR CVs, fraud notes, etc.
    """

    # Use a fixed seed for reproducible clustering.
    kmeans = KMeans(n_clusters=n_clusters, n_init="auto", random_state=42)
    labels = kmeans.fit_predict(points)
    return labels
