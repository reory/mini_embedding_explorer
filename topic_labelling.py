"""Generate simple human-readable labels for text clusters."""

import re
from collections import Counter, defaultdict

STOPWORDS = {
    "a", "an", "and", "are", "as", "at",
    "be", "for", "from", "in", "is",
    "it", "of", "on", "or", "that", "the",
    "to", "was", "were", "with",
    "can", "cannot", "could", "should",
    "would", "will", "still", "very",
    "too", "into", "when", "after",
    "before", "again",
    "app", "application", "system",
    "issue", "issues", "problem",
    "problems", "error", "errors",
    "team", "service", "support",
}

def clean_words(text):
    """Extract meaningful words from a text string."""

    words = re.findall(r"\b[a-zA-Z]+\b", text.lower())

    return [
        word 
        for word in words 
        if word not in STOPWORDS and len(word) > 2
    ]   


def extract_keywords(texts, top_n=4):
    """Return the most common keywords from a collection of texts."""

    counter = Counter()

    for text in texts:
        counter.update(clean_words(text))

    return [word for word, _ in counter.most_common(top_n)]


def generate_cluster_labels(texts, labels):
    """Generate a descriptive label cluster."""

    cluster_texts = defaultdict(list)

    # Group text by cluster.
    for text, label in zip(texts, labels):
        cluster_texts[label].append(text)

    cluster_labels = {}

    for cluster_id, cluster_entries in cluster_texts.items():

        keywords = extract_keywords(cluster_entries)

        if keywords:
            cluster_labels[cluster_id] = " ".join(
                word.title() for word in keywords
            )
        else:
            cluster_labels[cluster_id] = f"Cluster{cluster_id}"

    return cluster_labels
