def adaptive_signal(row):
    if row["regime"] == 0:
        return row["ma_signal"]
    elif row["regime"] == 2:
        return row["rsi_signal"]
    else:
        return (row["ma_signal"] + row["rsi_signal"] + row["bb_signal"]) / 3
