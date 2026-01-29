import matplotlib.pyplot as plt

def plot_regime_band(feature_data):
    fig, ax = plt.subplots(figsize=(10, 2))

    regime_colors = {
        0: "green",
        1: "orange",
        2: "red"
    }

    dates = feature_data.index
    regimes = feature_data["regime"].values

    for i in range(len(dates) - 1):
        ax.axvspan(
            dates[i],
            dates[i + 1],
            color=regime_colors[regimes[i]],
            alpha=0.6
        )

    ax.set_yticks([])
    ax.set_title("Market Regime Timeline (Behavioral States)")
    ax.set_xlabel("Date")

    return fig



