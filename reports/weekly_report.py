from datetime import date
from src.explain import explain_regime

def generate_weekly_report(current_regime):
    report = f"""
    WEEKLY MARKET REGIME REPORT
    Date: {date.today()}

    Current Regime: {current_regime}

    Interpretation:
    {explain_regime(current_regime)}

    Note:
    This report is based on historical regime behavior and is intended
    for decision support, not price prediction.
    """
    return report
