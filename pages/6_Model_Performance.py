import streamlit as st
import pandas as pd
import joblib
import plotly.express as px
from pathlib import Path

st.set_page_config(
    page_title="Model Performance",
    page_icon="📈",
    layout="wide"
)

# ============================================================
# CUSTOMERPULSE UI
# HealthTwin-inspired Lavender Theme
# Font: Patrick Hand
# ============================================================

st.markdown(
    """
    <style>

    @import url('https://fonts.googleapis.com/css2?family=Patrick+Hand&display=swap');

    /* -----------------------------
       GLOBAL FONT
    ----------------------------- */

    html,
    body,
    .stApp {
        font-family: 'Patrick Hand', sans-serif !important;
    }

    h1, h2, h3, h4, h5, h6,
    p,
    label,
    button,
    input,
    textarea,
    select,
    [data-testid="stMarkdownContainer"],
    [data-testid="stMetricValue"],
    [data-testid="stMetricLabel"] {
        font-family: 'Patrick Hand', sans-serif !important;
    }
    /* Keep Streamlit icons using their own icon font */
    .material-symbols-rounded,
    .material-symbols-outlined,
    [data-testid="stSidebarCollapseButton"] span,
    [data-testid="stSidebarCollapseButton"] * {
        font-family: "Material Symbols Rounded" !important;
    }

    /* -----------------------------
       PAGE
    ----------------------------- */

    .stApp {
        background: #F8F5FC;
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        padding-left: 3rem;
        padding-right: 3rem;
        max-width: 1250px;
    }

    /* -----------------------------
       HEADER CARD
    ----------------------------- */

    .cp-header-card {
        background: #EDE3F8;
        border: 1px solid #D8C5ED;
        border-radius: 20px;
        padding: 25px 30px;
        margin-bottom: 30px;
        box-shadow: 0 6px 20px rgba(91, 58, 142, 0.08);
    }

    .cp-header-title {
        color: #56327F;
        font-size: 32px;
        font-weight: 800;
        line-height: 1.2;
        margin: 0;
    }

    .cp-header-subtitle {
        color: #78698A;
        font-size: 14px;
        margin-top: 7px;
    }

    /* -----------------------------
       SECTION HEADING
    ----------------------------- */

    .cp-section {
        color: #56327F;
        font-size: 22px;
        font-weight: 700;
        margin-top: 20px;
        margin-bottom: 18px;
    }

    /* -----------------------------
       CONTENT CARDS
    ----------------------------- */

    .cp-card {
        background: #EDE3F8;
        border: 1px solid #D8C5ED;
        border-radius: 18px;
        padding: 22px;
        margin-bottom: 22px;
        box-shadow: 0 5px 18px rgba(91, 58, 142, 0.07);
    }

    /* -----------------------------
       METRIC CARD
    ----------------------------- */

    .cp-metric-card {
        background: #EDE3F8;
        border: 1px solid #D8C5ED;
        border-radius: 18px;
        padding: 20px;
        text-align: center;
        min-height: 120px;
        box-shadow: 0 5px 18px rgba(91, 58, 142, 0.07);
    }

    .cp-metric-label {
        color: #78698A;
        font-size: 16px;
        margin-bottom: 5px;
    }

    .cp-metric-value {
        color: #4B286F;
        font-size: 30px;
        font-weight: 800;
    }

    /* -----------------------------
       INFO CARD
    ----------------------------- */

    .cp-info-card {
        background: #EDE3F8;
        border: 1px solid #D8C5ED;
        border-radius: 18px;
        padding: 24px;
        box-shadow: 0 5px 18px rgba(91, 58, 142, 0.07);
    }

    .cp-info-title {
        color: #56327F;
        font-size: 20px;
        font-weight: 800;
        margin-bottom: 12px;
    }

    .cp-info-text {
        color: #78698A;
        font-size: 16px;
        line-height: 1.5;
    }

    .cp-info-text strong {
        color: #4B286F;
    }

    /* -----------------------------
       DATAFRAME
    ----------------------------- */

    div[data-testid="stDataFrame"] {
        border-radius: 12px;
        overflow: hidden;
    }

    div[data-testid="stDataFrame"],
    div[data-testid="stDataFrame"] * {
        font-family: 'Patrick Hand', sans-serif !important;
    }

    /* -----------------------------
       PLOTLY
    ----------------------------- */

    .js-plotly-plot,
    .plot-container {
        border-radius: 14px;
    }

    /* -----------------------------
       DIVIDER
    ----------------------------- */

    .cp-divider {
        height: 1px;
        background: #DDD0EA;
        margin: 30px 0;
    }

    /* -----------------------------
       SUCCESS / INFO
    ----------------------------- */

    div[data-testid="stAlert"] {
        border-radius: 15px !important;
        border: 1px solid #D8C5ED !important;
    }

    div[data-testid="stAlert"] * {
        font-family: 'Patrick Hand', sans-serif !important;
    }

    /* -----------------------------
       FOOTER
    ----------------------------- */

    .cp-footer {
        background: #EDE3F8;
        border: 1px solid #D8C5ED;
        border-radius: 18px;
        padding: 22px;
        margin-top: 30px;
        text-align: center;
        box-shadow: 0 5px 18px rgba(91, 58, 142, 0.07);
    }

    .cp-footer-title {
        color: #56327F;
        font-size: 18px;
        font-weight: 800;
    }

    .cp-footer-text {
        color: #78698A;
        font-size: 13px;
        margin-top: 6px;
    }

    /* -----------------------------
       STREAMLIT DEFAULTS
    ----------------------------- */

    header[data-testid="stHeader"] {
        background: transparent !important;
    }

    footer {
        visibility: hidden;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# PAGE HEADER
# ============================================================

st.html(
    """
    <div class="cp-header-card">

        <div class="cp-header-title">
            📈 Model Performance Analysis
        </div>

        <div class="cp-header-subtitle">
            Compare churn prediction models and understand
            the features influencing customer churn.
        </div>

    </div>
    """
)


# ============================================================
# PATHS
# ============================================================

BASE_DIR = Path(__file__).resolve().parent.parent
MODELS = BASE_DIR / "models"


# ============================================================
# LOAD MODEL FILES
# ============================================================

scores = joblib.load(
    MODELS / "model_scores.pkl"
)

feature_names = joblib.load(
    MODELS / "features.pkl"
)

feature_importance = joblib.load(
    MODELS / "feature_importance.pkl"
)

best_model = max(
    scores,
    key=scores.get
)


# ============================================================
# BEST MODEL SUMMARY
# ============================================================

st.html(
    """
    <div class="cp-section">
        🏆 Best Model Summary
    </div>
    """
)

col1, col2 = st.columns(2)

with col1:

    st.html(
        f"""
        <div class="cp-metric-card">

            <div class="cp-metric-label">
                Best Model
            </div>

            <div class="cp-metric-value">
                {best_model}
            </div>

        </div>
        """
    )

with col2:

    st.html(
        f"""
        <div class="cp-metric-card">

            <div class="cp-metric-label">
                Best Accuracy
            </div>

            <div class="cp-metric-value">
                {scores[best_model] * 100:.2f}%
            </div>

        </div>
        """
    )


# ============================================================
# MODEL COMPARISON
# ============================================================

st.html(
    """
    <div class="cp-section">
        📊 Model Comparison
    </div>
    """
)

comparison = pd.DataFrame(
    {
        "Model": list(scores.keys()),
        "Accuracy": [
            round(value * 100, 2)
            for value in scores.values()
        ]
    }
)

with st.container(border=True):

    st.dataframe(
        comparison,
        use_container_width=True
    )


# ============================================================
# ACCURACY CHART
# ============================================================

with st.container(border=True):

    fig = px.bar(
        comparison,
        x="Model",
        y="Accuracy",
        text="Accuracy",
        color="Model",
        title="Accuracy Comparison"
    )

    fig.update_traces(
        textposition="outside"
    )

    fig.update_layout(
        plot_bgcolor="#EDE3F8",
        paper_bgcolor="#EDE3F8",
        font=dict(
            family="Patrick Hand",
            color="#56327F"
        ),
        title_font=dict(
            family="Patrick Hand",
            color="#56327F"
        ),
        xaxis=dict(
            title="Model",
            title_font=dict(
                family="Patrick Hand",
                color="#56327F"
            )
        ),
        yaxis=dict(
            title="Accuracy (%)",
            title_font=dict(
                family="Patrick Hand",
                color="#56327F"
            )
        )
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# ============================================================
# FEATURE IMPORTANCE
# ============================================================

st.html(
    """
    <div class="cp-section">
        ⭐ Feature Importance
    </div>
    """
)

importance = pd.DataFrame(
    {
        "Feature": feature_names,
        "Importance": feature_importance
    }
)

importance = importance.sort_values(
    "Importance",
    ascending=False
)


with st.container(border=True):

    st.dataframe(
        importance,
        use_container_width=True
    )


# ============================================================
# FEATURE IMPORTANCE CHART
# ============================================================

with st.container(border=True):

    fig = px.bar(
        importance,
        x="Importance",
        y="Feature",
        orientation="h",
        title="Feature Importance"
    )

    fig.update_layout(
        plot_bgcolor="#EDE3F8",
        paper_bgcolor="#EDE3F8",
        font=dict(
            family="Patrick Hand",
            color="#56327F"
        ),
        title_font=dict(
            family="Patrick Hand",
            color="#56327F"
        ),
        xaxis=dict(
            title="Importance",
            title_font=dict(
                family="Patrick Hand",
                color="#56327F"
            )
        ),
        yaxis=dict(
            title="Feature",
            title_font=dict(
                family="Patrick Hand",
                color="#56327F"
            )
        )
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )


# ============================================================
# BEST MODEL DETAILS
# ============================================================

st.html(
    """
    <div class="cp-section">
        🏆 Best Model Details
    </div>
    """
)

st.html(
    f"""
    <div class="cp-info-card">

        <div class="cp-info-title">
            Selected Model Information
        </div>

        <div class="cp-info-text">

            <strong>Selected Model:</strong>
            {best_model}

            <br><br>

            <strong>Accuracy:</strong>
            {scores[best_model] * 100:.2f}%

            <br><br>

            The model was selected automatically by comparing
            the accuracy of Decision Tree, Random Forest and XGBoost.

            <br><br>

            The highest accuracy model is saved and used
            throughout the application for churn prediction.

        </div>

    </div>
    """
)


# ============================================================
# FOOTER
# ============================================================

st.html(
    """
    <div class="cp-footer">

        <div class="cp-footer-title">
            💜 CustomerPulse
        </div>

        <div class="cp-footer-text">
            Customer Churn Analytics & Retention System
        </div>

    </div>
    """
)
