def rsi_signal(rsi):
    if rsi < 30:
        return 1
    elif rsi > 70:
        return -1
    return 0


def ma_signal(fast_ma, slow_ma):
    if fast_ma > slow_ma:
        return 1
    elif fast_ma < slow_ma:
        return -1
    return 0


def bb_signal(close, lower_band, upper_band):
    if close < lower_band:
        return 1
    elif close > upper_band:
        return -1
    return 0


