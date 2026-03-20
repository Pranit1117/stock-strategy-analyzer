import numpy as np
from src.features import build_features
from src.regimes import kmeans_numpy

def compute_current_regime(price_df, k=3):
    """
    Compute current market regime from recent data
    """
    features = build_features(price_df)

    X = features.values
    labels = kmeans_numpy(X, k=k)

    # Attach regime labels
    features["regime"] = labels

    # Most recent regime
    current_regime = int(features["regime"].iloc[-1])

    return current_regime, features
