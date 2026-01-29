def explain_regime(regime, stats=None):
    if regime == 0:
        return (
            "The market is currently in a trending regime. "
            "Historically, trend-following strategies such as moving averages "
            "performed better, while mean-reversion strategies underperformed."
        )

    elif regime == 2:
        return (
            "The market is in a volatile or mean-reverting regime. "
            "In similar conditions, momentum exhaustion strategies like RSI "
            "showed better robustness, while trend-following strategies struggled."
        )

    else:
        return (
            "The market is in a mixed or transitional regime. "
            "No single strategy consistently dominated in the past. "
            "A blended or risk-aware approach is recommended."
        )
