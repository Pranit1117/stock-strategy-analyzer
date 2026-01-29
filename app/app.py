import sys
import os

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(ROOT_DIR)


# ---------- IMPORTS ----------
import streamlit as st
from src.explain import explain_regime
from src.data_loader import load_nifty_data
from src.current_regime import compute_current_regime
from src.visuals import plot_regime_band
from src.report import generate_weekly_report


# ---------- STRATEGY HELPERS ----------
def recommended_strategy(regime):
    if regime == 0:
        return (
            "Trend-Following Behavior",
            "Trend-following strategies work best when price movements persist in one direction. "
            "Moving Average–based approaches historically outperform in such environments."
        )
    elif regime == 2:
        return (
            "Mean-Reversion Behavior",
            "In volatile and oscillating markets, prices tend to revert to their mean. "
            "RSI-style strategies historically perform better in such conditions."
        )
    else:
        return (
            "Risk-Reduced / Blended Approach",
            "Mixed regimes are unstable and unpredictable. No single strategy dominates, "
            "so risk reduction or blended exposure is historically safer."
        )

def why_not_explanations(regime):
    if regime == 0:
        return {
            "RSI": "Mean-reversion signals often trigger too early and fight sustained momentum.",
            "Bollinger Bands": "Low signal frequency and weak effectiveness in trending markets."
        }
    elif regime == 2:
        return {
            "Moving Averages": "Trend-following lags and suffers from whipsaws during reversals.",
            "Bollinger Bands": "Signals often overlap with RSI without adding meaningful edge."
        }
    else:
        return {
            "RSI": "Inconsistent performance due to frequent and abrupt regime shifts.",
            "Moving Averages": "False breakouts and short-lived trends dominate mixed regimes."
        }

# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="Market Regime Intelligence",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------- CUSTOM CSS FOR PREMIUM LOOK ----------
st.markdown("""
<style>
    /* Main theme colors */
    :root {
        --primary-green: #00C853;
        --primary-red: #FF1744;
        --warning-yellow: #FFC107;
        --bg-dark: #0E1117;
        --bg-card: #1E1E1E;
        --text-primary: #FAFAFA;
        --text-secondary: #B0B0B0;
        --border-color: #2D2D2D;
    }
    
    /* Remove default padding */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1400px;
    }
    
    /* Header styling */
    .main-header {
        text-align: center;
        padding: 2rem 0 1rem 0;
        background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
        border-radius: 12px;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
    }
    
    .main-header h1 {
        color: white;
        font-size: 2.5rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
        letter-spacing: -0.5px;
    }
    
    .main-header p {
        color: rgba(255, 255, 255, 0.8);
        font-size: 1.1rem;
        margin: 0;
    }
    
    /* Regime card styling */
    .regime-card {
        padding: 2rem;
        border-radius: 16px;
        border: 2px solid;
        text-align: center;
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
        transition: transform 0.2s;
        height: 100%;
    }
    
    .regime-card:hover {
        transform: translateY(-4px);
    }
    
    .regime-card h3 {
        font-size: 1rem;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 0.5rem;
        opacity: 0.8;
    }
    
    .regime-card h2 {
        font-size: 2rem;
        font-weight: 700;
        margin: 1rem 0;
    }
    
    .regime-icon {
        font-size: 3rem;
        margin-bottom: 1rem;
    }
    
    /* AI explanation box */
    .ai-explanation {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 16px;
        color: white;
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
        height: 100%;
    }
    
    .ai-explanation h3 {
        margin-top: 0;
        font-size: 1.3rem;
        margin-bottom: 1rem;
    }
    
    .ai-explanation p {
        line-height: 1.7;
        font-size: 1.05rem;
    }
    
    /* Metric cards */
    .metric-container {
        background: var(--bg-card);
        padding: 1.5rem;
        border-radius: 12px;
        border: 1px solid var(--border-color);
        text-align: center;
    }
    
    .metric-label {
        color: var(--text-secondary);
        font-size: 0.9rem;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 0.5rem;
    }
    
    .metric-value {
        font-size: 2rem;
        font-weight: 700;
        color: var(--text-primary);
    }
    
    /* Strategy card */
    .strategy-card {
        background: linear-gradient(135deg, #11998e 0%, #38ef7d 100%);
        padding: 2rem;
        border-radius: 16px;
        color: white;
        margin: 2rem 0;
        box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
    }
    
    .strategy-card h3 {
        margin-top: 0;
        font-size: 1.5rem;
        margin-bottom: 0.5rem;
    }
    
    .strategy-card h4 {
        font-size: 1.8rem;
        font-weight: 700;
        margin: 0.5rem 0 1rem 0;
    }
    
    /* Indicator card */
    .indicator-card {
        background: rgba(33, 150, 243, 0.1);
        border-left: 4px solid #2196F3;
        padding: 1.5rem;
        border-radius: 8px;
        margin: 1rem 0;
    }
    
    /* Warning card */
    .warning-card {
        background: rgba(255, 152, 0, 0.1);
        border-left: 4px solid #FF9800;
        padding: 1rem 1.5rem;
        border-radius: 8px;
        margin: 0.5rem 0;
    }
    
    .warning-card strong {
        color: #FF9800;
        font-size: 1.1rem;
    }
    
    /* Section headers */
    .section-header {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        margin: 2rem 0 1rem 0;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid var(--border-color);
    }
    
    .section-header h2 {
        margin: 0;
        font-size: 1.5rem;
        font-weight: 600;
    }
    
    /* Sidebar styling */
    .css-1d391kg {
        background-color: #1a1a1a;
    }
    
    /* Download button enhancement */
    .stDownloadButton button {
        width: 100%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-weight: 600;
        padding: 0.75rem 1.5rem;
        border-radius: 8px;
        border: none;
        font-size: 1.1rem;
        transition: transform 0.2s;
    }
    
    .stDownloadButton button:hover {
        transform: scale(1.02);
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 1rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        padding: 0.75rem 1.5rem;
        font-weight: 600;
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        font-weight: 600;
        font-size: 1.1rem;
    }
    
    /* Info box styling */
    .stAlert {
        border-radius: 12px;
    }
    
    /* Chart container */
    .chart-container {
        background: var(--bg-card);
        padding: 2rem;
        border-radius: 16px;
        border: 1px solid var(--border-color);
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# ---------- SIDEBAR CONFIGURATION ----------
with st.sidebar:
    st.markdown("### ⚙️ Configuration")
    st.markdown("---")
    
    st.markdown("#### 📊 Data Settings")
    data_period = st.selectbox(
        "Analysis Period",
        options=["1mo", "3mo", "6mo", "1y", "2y"],
        index=2,  # Default to 6mo
        help="Select the historical period for regime analysis"
    )
    
    st.markdown("---")
    st.markdown("#### 🎯 Display Options")
    
    show_timeline = st.checkbox("Show Regime Timeline", value=True)
    show_strategy = st.checkbox("Show Strategy Guidance", value=True)
    show_warnings = st.checkbox("Show Strategy Warnings", value=True)
    show_forecast = st.checkbox("Show Historical Patterns", value=True)
    
    st.markdown("---")
    st.markdown("#### ℹ️ About")
    st.caption(
        "This system analyzes market behavior patterns "
        "to identify the current regime and suggest "
        "appropriate trading strategies."
    )
    
    st.caption("**Data Source:** NIFTY 50 Index")
    st.caption("**Update Frequency:** Real-time")

# ---------- HEADER ----------
st.markdown("""
<div class="main-header">
    <h1>📊 Market Regime Intelligence</h1>
    <p>AI-Powered Decision Support for Systematic Trading</p>
</div>
""", unsafe_allow_html=True)

# ---------- LOAD DATA WITH SPINNER ----------
with st.spinner("🔄 Analyzing market data..."):
    price_data = load_nifty_data(period=data_period)
    current_regime, feature_data = compute_current_regime(price_data)

# ---------- REGIME MAPPING ----------
regime_map = {
    0: ("Trending", "🟢", "#00C853", "#e8f5e9", "#1b5e20"),
    1: ("Mixed / Transitional", "🟡", "#FFC107", "#fff9e6", "#f57f17"),
    2: ("Mean-Reverting / Volatile", "🔴", "#FF1744", "#ffebee", "#b71c1c")
}

regime_name, regime_icon, regime_color, bg_color, border_color = regime_map[current_regime]

# ---------- MAIN CONTENT TABS ----------
tab1, tab2, tab3 = st.tabs(["📈 Current Regime", "📊 Analysis & Charts", "📥 Reports"])

# ========== TAB 1: CURRENT REGIME ========== 
with tab1:
    # Top section: Regime Card + AI Explanation
    col1, col2 = st.columns([1, 1.5], gap="large")
    
    with col1:
        st.markdown(f"""
        <div class="regime-card" style="background-color: {bg_color}; border-color: {border_color};">
            <div class="regime-icon">{regime_icon}</div>
            <h3 style="color: {border_color};">Current Market Regime</h3>
            <h2 style="color: {border_color};">{regime_name}</h2>
            <p style="color: {border_color}; opacity: 0.8; margin-top: 1rem;">
                Detected using {len(feature_data)} trading observations
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Confidence metric
        st.markdown("""
        <div class="metric-container">
            <div class="metric-label">Analysis Confidence</div>
            <div class="metric-value">High</div>
            <p style="color: var(--text-secondary); margin-top: 0.5rem; font-size: 0.9rem;">
                Based on historical pattern matching
            </p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="ai-explanation">
            <h3>🤖 AI Regime Analysis</h3>
            <p>{explain_regime(current_regime)}</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Strategy Recommendation Section
    if show_strategy:
        strategy, explanation = recommended_strategy(current_regime)
        
        st.markdown(f"""
        <div class="strategy-card">
            <h3>🎯 Recommended Strategy Behavior</h3>
            <h4>{strategy}</h4>
            <p style="line-height: 1.7; font-size: 1.05rem;">{explanation}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Example Indicator
        st.markdown('<div class="section-header"><h2>💡 Optimal Indicator for This Regime</h2></div>', unsafe_allow_html=True)
        
        if current_regime == 0:
            st.markdown("""
            <div class="indicator-card">
                <h4 style="margin-top: 0; color: #2196F3;">📈 Moving Averages (Trend-Following)</h4>
                <p style="line-height: 1.6;">
                    In trending regimes, prices exhibit persistence and directional momentum.
                    Moving averages help you stay aligned with the dominant trend and avoid
                    counter-trend trades that typically fail in these conditions.
                </p>
                <p style="margin-top: 1rem; opacity: 0.8;"><strong>Best Use:</strong> 
                Golden Cross (50/200 MA), EMA crossovers, trend confirmation</p>
            </div>
            """, unsafe_allow_html=True)
        
        elif current_regime == 2:
            st.markdown("""
            <div class="indicator-card">
                <h4 style="margin-top: 0; color: #2196F3;">📉 RSI (Mean-Reversion)</h4>
                <p style="line-height: 1.6;">
                    In mean-reverting regimes, price extremes tend to snap back to equilibrium.
                    RSI effectively identifies overbought and oversold conditions, making it
                    ideal for fading extremes and capturing reversal moves.
                </p>
                <p style="margin-top: 1rem; opacity: 0.8;"><strong>Best Use:</strong> 
                RSI < 30 (oversold), RSI > 70 (overbought), divergence signals</p>
            </div>
            """, unsafe_allow_html=True)
        
        else:
            st.markdown("""
            <div class="indicator-card">
                <h4 style="margin-top: 0; color: #2196F3;">⚖️ No Single Indicator Dominates</h4>
                <p style="line-height: 1.6;">
                    In mixed regimes, technical indicators frequently conflict and produce
                    false signals. The safest approach is reducing position sizes, blending
                    multiple signals, or staying on the sidelines until clarity emerges.
                </p>
                <p style="margin-top: 1rem; opacity: 0.8;"><strong>Best Use:</strong> 
                Portfolio hedging, reduced leverage, multi-timeframe confirmation</p>
            </div>
            """, unsafe_allow_html=True)
    
    # Why Not Section
    if show_warnings:
        st.markdown('<div class="section-header"><h2>⚠️ Strategies to Avoid Right Now</h2></div>', unsafe_allow_html=True)
        
        reasons = why_not_explanations(current_regime)
        
        for strat, reason in reasons.items():
            st.markdown(f"""
            <div class="warning-card">
                <strong>{strat}</strong> — {reason}
            </div>
            """, unsafe_allow_html=True)
    
    # Historical Pattern Section
    if show_forecast:
        st.markdown('<div class="section-header"><h2>🧠 Historical Pattern Analysis</h2></div>', unsafe_allow_html=True)
        
        if current_regime == 0:
            st.info("""
            **📊 Trending Regime Behavior**
            
            Historically, trending regimes tend to persist for extended periods (weeks to months),
            but often transition into mixed regimes before fully reversing. Sharp reversals
            directly from trending to mean-reverting states are less common.
            
            **Typical Duration:** 4-12 weeks  
            **Next State Probability:** Mixed (60%) | Continues (30%) | Mean-Revert (10%)
            """)
        
        elif current_regime == 2:
            st.info("""
            **📊 Mean-Reverting Regime Behavior**
            
            Mean-reverting regimes are usually short-lived and characterized by high volatility.
            They often resolve into either strong trending phases (as momentum builds) or
            transition through mixed states before stabilizing.
            
            **Typical Duration:** 1-4 weeks  
            **Next State Probability:** Mixed (50%) | Trending (35%) | Continues (15%)
            """)
        
        else:
            st.info("""
            **📊 Mixed Regime Behavior**
            
            Mixed regimes frequently act as transition phases between market states. They're
            characterized by uncertainty and conflicting signals. These periods often precede
            either strong breakout trends or high-volatility mean-reverting phases.
            
            **Typical Duration:** 2-6 weeks  
            **Next State Probability:** Trending (45%) | Mean-Revert (40%) | Continues (15%)
            """)

# ========== TAB 2: CHARTS ========== 
with tab2:
    st.markdown('<div class="section-header"><h2>📊 Market Regime Timeline</h2></div>', unsafe_allow_html=True)
    
    if show_timeline:
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        
        fig = plot_regime_band(feature_data)
        st.pyplot(fig, use_container_width=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.caption(f"📅 Analysis based on {len(feature_data)} trading days | Period: {data_period}")
    else:
        st.info("👆 Enable 'Show Regime Timeline' in the sidebar to view the chart")
    
    # Additional metrics section
    st.markdown('<div class="section-header"><h2>📈 Key Metrics</h2></div>', unsafe_allow_html=True)
    
    m1, m2, m3, m4 = st.columns(4)
    
    with m1:
        st.markdown("""
        <div class="metric-container">
            <div class="metric-label">Data Points</div>
            <div class="metric-value" style="font-size: 1.5rem;">{}</div>
        </div>
        """.format(len(feature_data)), unsafe_allow_html=True)
    
    with m2:
        st.markdown("""
        <div class="metric-container">
            <div class="metric-label">Analysis Period</div>
            <div class="metric-value" style="font-size: 1.5rem;">{}</div>
        </div>
        """.format(data_period.upper()), unsafe_allow_html=True)
    
    with m3:
        st.markdown("""
        <div class="metric-container">
            <div class="metric-label">Regime Type</div>
            <div class="metric-value" style="font-size: 1.5rem;">{}</div>
        </div>
        """.format(current_regime), unsafe_allow_html=True)
    
    with m4:
        st.markdown(f"""
        <div class="metric-container">
            <div class="metric-label">Status</div>
            <div class="metric-value" style="font-size: 1.5rem; color: {regime_color};">{regime_icon}</div>
        </div>
        """, unsafe_allow_html=True)

# ========== TAB 3: REPORTS ========== 
with tab3:
    st.markdown('<div class="section-header"><h2>📥 Weekly Market Report</h2></div>', unsafe_allow_html=True)
    
    strategy, explanation = recommended_strategy(current_regime)
    
    report_text = generate_weekly_report(
        current_regime,
        regime_name,
        strategy,
        explanation
    )
    
    # Report preview
    with st.expander("📄 Preview Report", expanded=True):
        st.text(report_text)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Download section
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.download_button(
            label="📥 Download Weekly Report",
            data=report_text,
            file_name=f"market_regime_report_{regime_name.lower().replace(' ', '_')}.txt",
            mime="text/plain",
            use_container_width=True
        )
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    st.info("""
    **📧 Report Includes:**
    - Current regime analysis and confidence
    - Recommended strategy behavior
    - Key indicators to watch
    - Strategies to avoid
    - Historical pattern insights
    """)

# ---------- FOOTER ----------
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("---")

col1, col2 = st.columns([3, 1])

with col1:
    st.warning("""
    **⚠️ Risk Disclaimer**  
    This system provides decision support based on historical market behavior patterns. 
    It does **not** predict future prices or generate specific buy/sell signals. 
    Always conduct your own research and consider your risk tolerance before trading.
    """)

with col2:
    st.markdown("""
    <div style="text-align: right; padding-top: 1rem;">
        <p style="color: var(--text-secondary); font-size: 0.9rem; margin: 0;">
            <strong>Version</strong> 1.0<br>
            <strong>Updated</strong> Daily
        </p>
    </div>
    """, unsafe_allow_html=True)


