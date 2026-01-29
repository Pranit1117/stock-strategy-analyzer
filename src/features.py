import pandas as pd

def build_features(df):
    features = pd.DataFrame(index=df.index)

    features["returns"] = df["Close"].pct_change()
    features["volatility_20"] = features["returns"].rolling(20).std()
    features["trend_strength"] = df["Close"] / df["Close"].rolling(50).mean() - 1
    features["range_20"] = (df["High"] - df["Low"]).rolling(20).mean()

    return features.dropna()
