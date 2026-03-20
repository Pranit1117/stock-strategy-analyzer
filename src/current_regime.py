import numpy as np
from src.features import build_features
from src.regimes import kmeans_numpy

def compute_current_regime(price_df, k=3):
    """
    Compute current market regime from recent data.
    Always returns a regime in {0, 1, 2} regardless of data length.
    """
    features = build_features(price_df)
    X = features.values

    # If not enough data after feature engineering, default to Mixed (1)
    if len(X) < 2:
        features["regime"] = 1
        return 1, features

    effective_k = min(k, len(X))
    labels = kmeans_numpy(X, k=k)

    # Remap labels to always stay within {0, 1, 2}
    if effective_k < 3:
        if effective_k == 1:
            remap = {0: 1}
        else:  # effective_k == 2
            remap = {0: 0, 1: 2}
        labels = np.array([remap[l] for l in labels])

    features["regime"] = labels
    current_regime = int(features["regime"].iloc[-1])
    return current_regime, features
