import streamlit as st
import plotly.express as px
from database.db_connection import run_query

st.set_page_config(
    page_title="CustomerPulse Dashboard",
    page_icon="📊",
    layout="wide"
)

# ============================================================
# CUSTOMERPULSE GLOBAL UI
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
       PAGE HEADER CARD
    ======================================================== */

    .cp-header-card {
        background: #EDE3F8;
        border: 1px solid #D8C5ED;
        border-radius: 20px;

        padding: 25px 30px;
        margin-bottom: 30px;

        box-shadow:
            0 6px 20px rgba(91, 58, 142, 0.08);
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
        font-weight: 500;
        margin-top: 7px;
    }


    /* ========================================================
       SECTION HEADINGS
    ======================================================== */

    .cp-section {
        color: #56327F;
        font-size: 22px;
        font-weight: 750;

        margin-top: 18px;
        margin-bottom: 18px;
    }


    /* ========================================================
       KPI CARDS
    ======================================================== */

    .cp-kpi {
        background: #EDE3F8;
        border: 1px solid #D8C5ED;
        border-radius: 18px;

        padding: 22px 22px 20px 22px;

        min-height: 125px;

        box-shadow:
            0 5px 18px rgba(91, 58, 142, 0.07);

        transition:
            transform 0.2s ease,
            box-shadow 0.2s ease;
    }

    .cp-kpi:hover {
        transform: translateY(-3px);

        box-shadow:
            0 9px 25px rgba(91, 58, 142, 0.12);
    }

    .cp-kpi-label {
        color: #766783;
        font-size: 13px;
        font-weight: 600;
        margin-bottom: 10px;
    }

    .cp-kpi-value {
        color: #4B286F;
        font-size: 28px;
        font-weight: 800;
        line-height: 1.2;
    }

    .cp-kpi-info {
        color: #9689A1;
        font-size: 12px;
        margin-top: 8px;
    }


    /* ========================================================
       STREAMLIT BORDERED CONTAINERS
       CHART CARDS
    ======================================================== */

    div[data-testid="stVerticalBlockBorderWrapper"] {
        background: #EDE3F8 !important;

        border: 1px solid #D8C5ED !important;

        border-radius: 18px !important;

        box-shadow:
            0 5px 18px rgba(91, 58, 142, 0.07);

        padding: 8px !important;
    }


    /* ========================================================
       DIVIDER
    ======================================================== */

    .cp-divider {
        height: 1px;
        background: #DDD0EA;
        margin: 30px 0;
    }


    /* ========================================================
       FOOTER CARD
    ======================================================== */

    .cp-footer {
        background: #EDE3F8;
        border: 1px solid #D8C5ED;
        border-radius: 18px;

        padding: 22px;
        margin-top: 30px;

        text-align: center;

        box-shadow:
            0 5px 18px rgba(91, 58, 142, 0.07);
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


    /* ========================================================
       STREAMLIT BUTTONS
    ======================================================== */

    .stButton > button {
        border-radius: 12px !important;

        border: 1px solid #D1BCE8 !important;

        background: #EDE3F8 !important;

        color: #56327F !important;

        font-family: 'Patrick Hand', sans-serif !important;

        font-weight: 700 !important;
    }

    .stButton > button:hover {
        border-color: #B99BD8 !important;

        background: #E3D5F2 !important;

        color: #4B286F !important;
    }


    /* ========================================================
       REMOVE EXTRA TOP SPACE
    ======================================================== */

    header[data-testid="stHeader"] {
        background: transparent;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# PAGE HEADER CARD
# ============================================================

st.html(
    """
    <div class="cp-header-card">

        <div class="cp-header-title">
            📊 CustomerPulse
        </div>

        <div class="cp-header-subtitle">
            Customer Analysis and Retention System
        </div>

    </div>
    """
)


# ============================================================
# KPI DATA
# ============================================================

total_result = run_query("""
    SELECT COUNT(*) AS Total
    FROM customer_data
""")

total_customers = int(
    total_result.iloc[0]["Total"]
)


churn_result = run_query("""
    SELECT COUNT(*) AS Churned
    FROM customer_data
    WHERE LOWER(TRIM(CAST(Churn AS CHAR))) IN
          ('1', 'yes', 'y', 'true')
""")

churn_customers = int(
    churn_result.iloc[0]["Churned"]
)


active_customers = (
    total_customers - churn_customers
)


if total_customers > 0:

    churn_rate = (
        churn_customers /
        total_customers
    ) * 100

else:

    churn_rate = 0


# ============================================================
# CUSTOMER SUMMARY
# ============================================================

st.html(
    """
    <div class="cp-section">
        📌 Customer Summary
    </div>
    """
)


col1, col2, col3, col4 = st.columns(4)


# ============================================================
# TOTAL CUSTOMERS
# ============================================================

with col1:

    st.html(
        f"""
        <div class="cp-kpi">

            <div class="cp-kpi-label">
                👥 Total Customers
            </div>

            <div class="cp-kpi-value">
                {total_customers:,}
            </div>

            <div class="cp-kpi-info">
                Customers in database
            </div>

        </div>
        """
    )


# ============================================================
# ACTIVE CUSTOMERS
# ============================================================

with col2:

    st.html(
        f"""
        <div class="cp-kpi">

            <div class="cp-kpi-label">
                🟢 Active Customers
            </div>

            <div class="cp-kpi-value">
                {active_customers:,}
            </div>

            <div class="cp-kpi-info">
                Currently not churned
            </div>

        </div>
        """
    )


# ============================================================
# CHURNED CUSTOMERS
# ============================================================

with col3:

    st.html(
        f"""
        <div class="cp-kpi">

            <div class="cp-kpi-label">
                🔴 Churned Customers
            </div>

            <div class="cp-kpi-value">
                {churn_customers:,}
            </div>

            <div class="cp-kpi-info">
                Customers marked as churned
            </div>

        </div>
        """
    )


# ============================================================
# CHURN RATE
# ============================================================

with col4:

    st.html(
        f"""
        <div class="cp-kpi">

            <div class="cp-kpi-label">
                📉 Churn Rate
            </div>

            <div class="cp-kpi-value">
                {churn_rate:.2f}%
            </div>

            <div class="cp-kpi-info">
                Overall customer churn
            </div>

        </div>
        """
    )


# ============================================================
# DIVIDER
# ============================================================

st.html(
    '<div class="cp-divider"></div>'
)


# ============================================================
# CUSTOMER ANALYTICS
# ============================================================

st.html(
    """
    <div class="cp-section">
        📈 Customer Analytics
    </div>
    """
)


# ============================================================
# SUBSCRIPTION PLAN
# ============================================================

subscription = run_query("""
    SELECT
        Subscription_Plan,
        COUNT(*) AS Customers
    FROM customer_data
    GROUP BY Subscription_Plan
    ORDER BY Customers DESC
""")


fig_subscription = px.bar(
    subscription,
    x="Subscription_Plan",
    y="Customers",
    text="Customers",
    title="Customers by Subscription Plan"
)

fig_subscription.update_traces(
    textposition="outside",
    marker_color="#B98EDC"
)

fig_subscription.update_layout(
    height=350,

    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",

    font=dict(
        family="Patrick Hand",
        size=12,
        color="#56327F"
    ),

    title_font=dict(
        family="Patrick Hand",
        size=17,
        color="#56327F"
    ),

    margin=dict(
        l=20,
        r=20,
        t=55,
        b=20
    ),

    showlegend=False
)


# ============================================================
# REGION DISTRIBUTION
# ============================================================

region = run_query("""
    SELECT
        Region,
        COUNT(*) AS Customers
    FROM customer_data
    GROUP BY Region
    ORDER BY Customers DESC
""")


fig_region = px.pie(
    region,
    names="Region",
    values="Customers",
    hole=0.45,
    title="Customers by Region"
)

fig_region.update_layout(
    height=350,

    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",

    font=dict(
        family="Patrick Hand",
        size=12,
        color="#56327F"
    ),

    title_font=dict(
        family="Patrick Hand",
        size=17,
        color="#56327F"
    ),

    margin=dict(
        l=20,
        r=20,
        t=55,
        b=20
    )
)


# ============================================================
# CHART ROW
# ============================================================

chart1, chart2 = st.columns(2)


# ============================================================
# SUBSCRIPTION CHART CARD
# ============================================================

with chart1:

    with st.container(border=True):

        st.plotly_chart(
            fig_subscription,
            width="stretch",
            config={
                "displayModeBar": False
            }
        )


# ============================================================
# REGION CHART CARD
# ============================================================

with chart2:

    with st.container(border=True):

        st.plotly_chart(
            fig_region,
            width="stretch",
            config={
                "displayModeBar": False
            }
        )


# ============================================================
# DEVICE DISTRIBUTION
# ============================================================

st.html(
    """
    <div class="cp-section">
        📱 Device Usage
    </div>
    """
)


device = run_query("""
    SELECT
        Device,
        COUNT(*) AS Customers
    FROM customer_data
    GROUP BY Device
    ORDER BY Customers DESC
""")


fig_device = px.bar(
    device,
    x="Device",
    y="Customers",
    text="Customers",
    title="Most Used Devices"
)

fig_device.update_traces(
    textposition="outside",
    marker_color="#B98EDC"
)

fig_device.update_layout(
    height=340,

    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",

    font=dict(
        family="Patrick Hand",
        size=12,
        color="#56327F"
    ),

    title_font=dict(
        family="Patrick Hand",
        size=17,
        color="#56327F"
    ),

    margin=dict(
        l=20,
        r=20,
        t=55,
        b=20
    ),

    showlegend=False
)


# ============================================================
# DEVICE CHART CARD
# ============================================================

with st.container(border=True):

    st.plotly_chart(
        fig_device,
        width="stretch",
        config={
            "displayModeBar": False
        }
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