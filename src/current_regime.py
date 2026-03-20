import numpy as np
from src.features import build_features
from src.regimes import kmeans_numpy

def compute_current_regime(price_df, k=3):
    """
    Compute current market regime from recent data.
    Always returns a regime in {0, 1, 2} regardless of how many
    clusters the data supports (handles short periods like 1mo).
    """
    features = build_features(price_df)
    X = features.values

    # effective_k may be less than k for short periods (e.g. 1mo)
    effective_k = min(k, len(X))
    labels = kmeans_numpy(X, k=k)  # reduction handled inside kmeans_numpy

    # Remap labels to always stay within {0, 1, 2} so app.py regime_map
    # never gets a KeyError when effective_k < 3
    if effective_k < 3:
        # effective_k=1 → all labels are 0 → remap to 1 (Mixed/Unknown)
        # effective_k=2 → labels 0,1 → remap to 0,2
        if effective_k == 1:
            remap = {0: 1}
        else:  # effective_k == 2
            remap = {0: 0, 1: 2}
        labels = np.array([remap[l] for l in labels])

    features["regime"] = labels
    current_regime = int(features["regime"].iloc[-1])
    return current_regime, features
