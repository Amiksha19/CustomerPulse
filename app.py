import streamlit as st

st.set_page_config(
    page_title="CustomerPulse",
    page_icon="📊",
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

    /* ========================================================
       GLOBAL FONT
    ======================================================== */

    html,
    body,
    .stApp,
    [data-testid="stAppViewContainer"],
    [data-testid="stSidebar"],
    button,
    input,
    textarea,
    select,
    option {
        font-family: 'Patrick Hand', sans-serif !important;
    }


    /* ========================================================
       PAGE BACKGROUND
    ======================================================== */

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


    /* ========================================================
       HERO / HEADER CARD
    ======================================================== */

    .cp-hero {
        background: #EDE3F8;
        border: 1px solid #D8C5ED;
        border-radius: 22px;

        padding: 35px 35px;
        margin-bottom: 30px;

        box-shadow:
            0 6px 20px rgba(91, 58, 142, 0.08);
    }

    .cp-hero-title {
        color: #56327F;
        font-size: 38px;
        font-weight: 800;
        line-height: 1.15;
        margin: 0;
    }

    .cp-hero-subtitle {
        color: #78698A;
        font-size: 18px;
        line-height: 1.5;
        margin-top: 12px;
        max-width: 850px;
    }


    /* ========================================================
       SECTION HEADING
    ======================================================== */

    .cp-section {
        color: #56327F;
        font-size: 25px;
        font-weight: 700;

        margin-top: 25px;
        margin-bottom: 18px;
    }


    /* ========================================================
       FEATURE CARDS
    ======================================================== */

    .cp-feature-card {
        background: #EDE3F8;
        border: 1px solid #D8C5ED;
        border-radius: 18px;

        padding: 24px;
        min-height: 190px;

        box-shadow:
            0 5px 18px rgba(91, 58, 142, 0.07);

        transition: 0.2s ease;
    }

    .cp-feature-card:hover {
        transform: translateY(-4px);

        box-shadow:
            0 9px 24px rgba(91, 58, 142, 0.12);
    }

    .cp-feature-icon {
        font-size: 32px;
        margin-bottom: 10px;
    }

    .cp-feature-title {
        color: #56327F;
        font-size: 21px;
        font-weight: 800;
        margin-bottom: 8px;
    }

    .cp-feature-text {
        color: #78698A;
        font-size: 15px;
        line-height: 1.5;
    }


    /* ========================================================
       WORKFLOW CARD
    ======================================================== */

    .cp-workflow-card {
        background: #EDE3F8;
        border: 1px solid #D8C5ED;
        border-radius: 18px;

        padding: 28px;

        box-shadow:
            0 5px 18px rgba(91, 58, 142, 0.07);
    }

    .cp-workflow-item {
        color: #56327F;
        font-size: 17px;
        font-weight: 600;

        padding: 12px 0;

        border-bottom: 1px solid #D8C5ED;
    }

    .cp-workflow-item:last-child {
        border-bottom: none;
    }

    .cp-workflow-number {
        display: inline-block;

        background: #D8C5ED;
        color: #4B286F;

        border-radius: 50%;

        width: 30px;
        height: 30px;

        text-align: center;
        line-height: 30px;

        margin-right: 10px;

        font-weight: 800;
    }


    /* ========================================================
       TECHNOLOGY CARD
    ======================================================== */

    .cp-tech-card {
        background: #EDE3F8;
        border: 1px solid #D8C5ED;
        border-radius: 18px;

        padding: 25px;

        text-align: center;

        box-shadow:
            0 5px 18px rgba(91, 58, 142, 0.07);
    }

    .cp-tech-title {
        color: #56327F;
        font-size: 19px;
        font-weight: 800;
    }

    .cp-tech-text {
        color: #78698A;
        font-size: 14px;
        margin-top: 6px;
    }


    /* ========================================================
       NAVIGATION CARD
    ======================================================== */

    .cp-navigation-card {
        background: #EDE3F8;
        border: 1px solid #D8C5ED;
        border-radius: 18px;

        padding: 25px;

        box-shadow:
            0 5px 18px rgba(91, 58, 142, 0.07);
    }

    .cp-navigation-text {
        color: #78698A;
        font-size: 16px;
        line-height: 1.6;
    }


    /* ========================================================
       DIVIDER
    ======================================================== */

    .cp-divider {
        height: 1px;
        background: #DDD0EA;
        margin: 35px 0;
    }


    /* ========================================================
       FOOTER
    ======================================================== */

    .cp-footer {
        background: #EDE3F8;
        border: 1px solid #D8C5ED;
        border-radius: 18px;

        padding: 22px;
        margin-top: 35px;

        text-align: center;

        box-shadow:
            0 5px 18px rgba(91, 58, 142, 0.07);
    }

    .cp-footer-title {
        color: #56327F;
        font-size: 20px;
        font-weight: 800;
    }

    .cp-footer-text {
        color: #78698A;
        font-size: 14px;
        margin-top: 6px;
    }


    /* ========================================================
       STREAMLIT DEFAULTS
    ======================================================== */

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
# HERO SECTION
# ============================================================

st.html(
    """
    <div class="cp-hero">

        <div class="cp-hero-title">
            📊 CustomerPulse
        </div>

        <div class="cp-hero-subtitle">
            Customer Churn Analytics &
            Retention System
        </div>

        <div class="cp-hero-subtitle">
            Analyze customer behavior, predict churn risk,
            understand customer patterns, and support
            data-driven retention decisions.
        </div>

    </div>
    """
)


# ============================================================
# WELCOME
# ============================================================

st.html(
    """
    <div class="cp-section">
        👋 Welcome to CustomerPulse
    </div>
    """
)

st.html(
    """
    <div class="cp-navigation-card">

        <div class="cp-navigation-text">

            CustomerPulse combines machine learning,
            database analytics, customer insights and
            retention management into one integrated
            customer retention platform.

            <br><br>

            Use the sections below to explore customer
            data, analyze churn patterns and manage
            customer follow-ups.

        </div>

    </div>
    """
)


# ============================================================
# MAIN FEATURES
# ============================================================

st.html(
    """
    <div class="cp-section">
        ✨ CustomerPulse Features
    </div>
    """
)

col1, col2 = st.columns(2)

with col1:

    st.html(
        """
        <div class="cp-feature-card">

            <div class="cp-feature-icon">
                📊
            </div>

            <div class="cp-feature-title">
                Customer Dashboard
            </div>

            <div class="cp-feature-text">
                Get an overview of customers, churn,
                subscription plans, regions and device
                usage through interactive analytics.
            </div>

        </div>
        """
    )


with col2:

    st.html(
        """
        <div class="cp-feature-card">

            <div class="cp-feature-icon">
                🤖
            </div>

            <div class="cp-feature-title">
                AI Churn Prediction
            </div>

            <div class="cp-feature-text">
                Analyze visitor, subscriber and existing
                customer information and predict customer
                churn risk using the trained machine
                learning model.
            </div>

        </div>
        """
    )


col3, col4 = st.columns(2)

with col3:

    st.html(
        """
        <div class="cp-feature-card">

            <div class="cp-feature-icon">
                👥
            </div>

            <div class="cp-feature-title">
                Customer Insights
            </div>

            <div class="cp-feature-text">
                Explore customer behavior, activity,
                demographics and churn-related patterns
                using database-driven analytics.
            </div>

        </div>
        """
    )


with col4:

    st.html(
        """
        <div class="cp-feature-card">

            <div class="cp-feature-icon">
                🎯
            </div>

            <div class="cp-feature-title">
                Retention System
            </div>

            <div class="cp-feature-text">
                Identify customers requiring attention,
                manage retention actions, and support
                customer re-engagement.
            </div>

        </div>
        """
    )


# ============================================================
# HOW CUSTOMERPULSE WORKS
# ============================================================

st.html(
    '<div class="cp-divider"></div>'
)

st.html(
    """
    <div class="cp-section">
        🔄 How CustomerPulse Works
    </div>
    """
)

st.html(
    """
    <div class="cp-workflow-card">

        <div class="cp-workflow-item">

            <span class="cp-workflow-number">
                1
            </span>

            Customer data is collected and stored
            in the MySQL database.

        </div>


        <div class="cp-workflow-item">

            <span class="cp-workflow-number">
                2
            </span>

            Customer behavior and profile information
            can be analyzed through the application.

        </div>


        <div class="cp-workflow-item">

            <span class="cp-workflow-number">
                3
            </span>

            The trained machine learning model evaluates
            customer churn risk.

        </div>


        <div class="cp-workflow-item">

            <span class="cp-workflow-number">
                4
            </span>

            Analytics pages provide customer and
            business insights.

        </div>


        <div class="cp-workflow-item">

            <span class="cp-workflow-number">
                5
            </span>

            Retention management supports customer
            follow-up and re-engagement activities.

        </div>

    </div>
    """
)


# ============================================================
# TECHNOLOGY STACK
# ============================================================

st.html(
    """
    <div class="cp-section">
        🛠️ Technology Used
    </div>
    """
)

tech1, tech2, tech3, tech4 = st.columns(4)

with tech1:

    st.html(
        """
        <div class="cp-tech-card">

            <div class="cp-tech-title">
                🐍 Python
            </div>

            <div class="cp-tech-text">
                Data Processing & ML
            </div>

        </div>
        """
    )


with tech2:

    st.html(
        """
        <div class="cp-tech-card">

            <div class="cp-tech-title">
                🤖 Machine Learning
            </div>

            <div class="cp-tech-text">
                Churn Prediction
            </div>

        </div>
        """
    )


with tech3:

    st.html(
        """
        <div class="cp-tech-card">

            <div class="cp-tech-title">
                🗄️ MySQL
            </div>

            <div class="cp-tech-text">
                Customer Database
            </div>

        </div>
        """
    )


with tech4:

    st.html(
        """
        <div class="cp-tech-card">

            <div class="cp-tech-title">
                📊 Streamlit
            </div>

            <div class="cp-tech-text">
                Interactive Web Application
            </div>

        </div>
        """
    )


# ============================================================
# QUICK NAVIGATION
# ============================================================

st.html(
    '<div class="cp-divider"></div>'
)

st.html(
    """
    <div class="cp-section">
        🧭 Quick Navigation
    </div>
    """
)

st.html(
    """
    <div class="cp-navigation-card">

        <div class="cp-navigation-text">

            📊 <strong>Dashboard</strong> —
            View overall customer and churn analytics.

            <br><br>

            🤖 <strong>Predict Churn</strong> —
            Analyze customers and generate churn predictions.

            <br><br>

            👥 <strong>Customer Insights</strong> —
            Explore customer behavior and database insights.

            <br><br>

            🎯 <strong>Retention System</strong> —
            Manage customer retention and re-engagement activities.

            <br><br>

            📈 <strong>Model Performance</strong> —
            Compare machine learning models and
            understand feature importance.

            <br><br>

            📊 <strong>SQL Analysis & Insights</strong> —
            Explore database-driven business analytics.

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
            Customer Churn Analytics &
            Retention System
        </div>

    </div>
    """
)