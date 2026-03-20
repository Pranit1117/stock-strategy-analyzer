import numpy as np

def kmeans_numpy(X, k=3, max_iters=100, seed=42):
    np.random.seed(seed)

    indices = np.random.choice(len(X), k, replace=False)
    centroids = X[indices]

    for _ in range(max_iters):
        distances = np.linalg.norm(X[:, None] - centroids, axis=2)
        labels = np.argmin(distances, axis=1)

        new_centroids = np.array([
            X[labels == i].mean(axis=0) for i in range(k)
        ])

        if np.allclose(centroids, new_centroids, atol=1e-4):
            break

        centroids = new_centroids

    return labels
