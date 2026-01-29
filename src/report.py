from datetime import date

def generate_weekly_report(regime, regime_name, strategy, explanation):
    today = date.today().strftime("%Y-%m-%d")

    report = f"""
WEEKLY MARKET REGIME REPORT
Date: {today}

Current Market Regime:
- {regime_name}

Recommended Strategy Behavior:
- {strategy}

Rationale:
{explanation}

Important Notes:
- Regimes are based on recent 20–50 trading days
- This is decision support, not price prediction
- No buy/sell signals are generated

Disclaimer:
This report is for educational and analytical purposes only.
"""

    return report
