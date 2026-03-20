import pandas as pd

def build_features(df):
    n = len(df)

    # Adaptive windows — scale down for short periods (e.g. 1mo ~22 days)
    w_short = min(20, max(2, n // 3))
    w_long  = min(50, max(3, n // 2))

    features = pd.DataFrame(index=df.index)
    features["returns"]        = df["Close"].pct_change()
    features["volatility_20"]  = features["returns"].rolling(w_short).std()
    features["trend_strength"] = df["Close"] / df["Close"].rolling(w_long).mean() - 1
    features["range_20"]       = (df["High"] - df["Low"]).rolling(w_short).mean()

    return features.dropna()
