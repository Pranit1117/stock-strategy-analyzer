import numpy as np

def kmeans_numpy(X, k=3, max_iters=100, seed=42):
    np.random.seed(seed)

    # Guard: can't have more clusters than data points
    k = min(k, len(X))

    if k == 0:
        return np.array([], dtype=int)

    indices = np.random.choice(len(X), k, replace=False)
    centroids = X[indices]

    for _ in range(max_iters):
        distances = np.linalg.norm(X[:, None] - centroids, axis=2)
        labels = np.argmin(distances, axis=1)
        new_centroids = np.array([
            # Guard: keep old centroid if cluster is empty
            X[labels == i].mean(axis=0) if np.any(labels == i) else centroids[i]
            for i in range(k)
        ])
        if np.allclose(centroids, new_centroids, atol=1e-4):
            break
        centroids = new_centroids

    return labels
