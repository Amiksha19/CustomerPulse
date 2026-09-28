import streamlit as st
import pandas as pd
import mysql.connector
import plotly.express as px

st.set_page_config(
    page_title="Customer Insights",
    page_icon="👥",
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
       HEADER CARD
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

        margin-top: 20px;
        margin-bottom: 18px;
    }


    /* ========================================================
       KPI CARDS
    ======================================================== */

    .cp-kpi {
        background: #EDE3F8;
        border: 1px solid #D8C5ED;
        border-radius: 18px;

        padding: 22px;

        min-height: 120px;

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
       CHART / TABLE CARDS
    ======================================================== */

    div[data-testid="stVerticalBlockBorderWrapper"] {
        background: #EDE3F8 !important;

        border: 1px solid #D8C5ED !important;

        border-radius: 18px !important;

        box-shadow:
            0 5px 18px rgba(91, 58, 142, 0.07);

        padding: 10px !important;
    }


    /* ========================================================
       DATAFRAME
    ======================================================== */

    div[data-testid="stDataFrame"] {
        border-radius: 12px;
        overflow: hidden;
    }


    /* ========================================================
       RECOMMENDATION CARD
    ======================================================== */

    .cp-recommendation {
        background: #EDE3F8;
        border: 1px solid #D8C5ED;
        border-radius: 15px;

        padding: 15px 18px;
        margin-bottom: 12px;

        color: #5A4A69;
        font-size: 14px;
        line-height: 1.6;

        box-shadow:
            0 3px 12px rgba(91, 58, 142, 0.05);
    }

    .cp-recommendation-number {
        color: #56327F;
        font-weight: 800;
        margin-right: 6px;
    }


    /* ========================================================
       INFO MESSAGE
    ======================================================== */

    div[data-testid="stAlert"] {
        border-radius: 15px !important;
        border: 1px solid #D8C5ED !important;
    }

    /* ========================================================
       HEALTH TWIN TYPOGRAPHY - PATRICK HAND
    ======================================================== */

    [data-testid="stMarkdownContainer"],
    [data-testid="stMarkdownContainer"] *,
    [data-testid="stWidgetLabel"],
    [data-testid="stWidgetLabel"] *,
    [data-testid="stCaptionContainer"],
    [data-testid="stDataFrame"],
    [data-testid="stDataFrame"] *,
    [data-testid="stMetric"],
    [data-testid="stMetric"] *,
    button,
    input,
    textarea,
    select,
    option {
        font-family: 'Patrick Hand', sans-serif !important;
    }

    .cp-header-title,
    .cp-header-subtitle,
    .cp-section,
    .cp-kpi-label,
    .cp-kpi-value,
    .cp-kpi-info,
    .cp-recommendation,
    .cp-recommendation-number {
        font-family: 'Patrick Hand', sans-serif !important;
    }



    /* ========================================================
       DIVIDER
    ======================================================== */

    .cp-divider {
        height: 1px;
        background: #DDD0EA;
        margin: 30px 0;
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# HEADER CARD
# ============================================================

st.html(
    """
    <div class="cp-header-card">

        <div class="cp-header-title">
            👥 Customer Insights
        </div>

        <div class="cp-header-subtitle">
            Explore customer behaviour and churn insights.
        </div>

    </div>
    """
)


# ============================================================
# DATABASE CONNECTION
# ============================================================

def get_connection():

    return mysql.connector.connect(
        host=st.secrets["mysql"]["host"],
        user=st.secrets["mysql"]["user"],
        password=st.secrets["mysql"]["password"],
        database=st.secrets["mysql"]["database"]
    )

# ============================================================
# LOAD CURRENT DATABASE DATA
# ============================================================

conn = get_connection()

cursor = conn.cursor()

cursor.execute("""
    SELECT *
    FROM customer_data
""")

rows = cursor.fetchall()

columns = [
    description[0]
    for description in cursor.description
]

cursor.close()
conn.close()

data = pd.DataFrame(
    rows,
    columns=columns
)


# ============================================================
# CHURN DISPLAY VALUE
# ============================================================

def normalize_churn(value):

    if pd.isna(value):
        return "Unknown"

    value = str(value).strip().lower()

    if value in [
        "1",
        "yes",
        "y",
        "true",
        "churn",
        "churned"
    ]:
        return "Yes"

    if value in [
        "0",
        "no",
        "n",
        "false",
        "active",
        "not churned"
    ]:
        return "No"

    return str(value)


data["Churn_Status"] = data["Churn"].apply(
    normalize_churn
)


# ============================================================
# KPIs
# ============================================================

total = len(data)

churned = len(
    data[
        data["Churn_Status"] == "Yes"
    ]
)

active = len(
    data[
        data["Churn_Status"] == "No"
    ]
)


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


col1, col2, col3 = st.columns(3)


# ------------------------------------------------------------
# TOTAL CUSTOMERS
# ------------------------------------------------------------

with col1:

    st.html(
        f"""
        <div class="cp-kpi">

            <div class="cp-kpi-label">
                👥 Total Customers
            </div>

            <div class="cp-kpi-value">
                {total:,}
            </div>

            <div class="cp-kpi-info">
                Customers in database
            </div>

        </div>
        """
    )


# ------------------------------------------------------------
# ACTIVE CUSTOMERS
# ------------------------------------------------------------

with col2:

    st.html(
        f"""
        <div class="cp-kpi">

            <div class="cp-kpi-label">
                🟢 Active Customers
            </div>

            <div class="cp-kpi-value">
                {active:,}
            </div>

            <div class="cp-kpi-info">
                Customers not marked as churned
            </div>

        </div>
        """
    )


# ------------------------------------------------------------
# CHURNED CUSTOMERS
# ------------------------------------------------------------

with col3:

    st.html(
        f"""
        <div class="cp-kpi">

            <div class="cp-kpi-label">
                🔴 Churned Customers
            </div>

            <div class="cp-kpi-value">
                {churned:,}
            </div>

            <div class="cp-kpi-info">
                Customers marked as churned
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
# AGE DISTRIBUTION
# ============================================================

st.html(
    """
    <div class="cp-section">
        📊 Age Distribution
    </div>
    """
)


fig_age = px.histogram(
    data,
    x="Age",
    color="Churn_Status",
    barmode="overlay",
    title="Age Distribution by Churn Status"
)

fig_age.update_layout(
    height=380,

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


with st.container(border=True):

    st.plotly_chart(
        fig_age,
        width="stretch",
        config={
            "displayModeBar": False
        }
    )


# ============================================================
# MONTHLY INCOME
# ============================================================

st.html(
    """
    <div class="cp-section">
        💰 Monthly Income
    </div>
    """
)


fig_income = px.box(
    data,
    x="Churn_Status",
    y="Monthly_Income",
    color="Churn_Status",
    title="Monthly Income by Churn Status"
)

fig_income.update_layout(
    height=380,

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


with st.container(border=True):

    st.plotly_chart(
        fig_income,
        width="stretch",
        config={
            "displayModeBar": False
        }
    )


# ============================================================
# REGION AND DEVICE
# ============================================================

st.html(
    """
    <div class="cp-section">
        🌍 Customer Distribution
    </div>
    """
)


# ============================================================
# REGION
# ============================================================

region = (
    data.groupby("Region")
    .size()
    .reset_index(name="Customers")
)


fig_region = px.bar(
    region,
    x="Region",
    y="Customers",
    color="Region",
    text="Customers",
    title="Customers by Region"
)

fig_region.update_traces(
    textposition="outside"
)

fig_region.update_layout(
    height=360,

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
# DEVICE
# ============================================================

device = (
    data.groupby("Device")
    .size()
    .reset_index(name="Customers")
)


fig_device = px.pie(
    device,
    names="Device",
    values="Customers",
    hole=0.4,
    title="Customer Device Usage"
)

fig_device.update_layout(
    height=360,

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
# TWO CHART CARDS
# ============================================================

chart1, chart2 = st.columns(2)


with chart1:

    with st.container(border=True):

        st.plotly_chart(
            fig_region,
            width="stretch",
            config={
                "displayModeBar": False
            }
        )


with chart2:

    with st.container(border=True):

        st.plotly_chart(
            fig_device,
            width="stretch",
            config={
                "displayModeBar": False
            }
        )


# ============================================================
# HIGH RISK CUSTOMERS
# ============================================================

st.html(
    """
    <div class="cp-section">
        ⚠️ High Risk Customers
    </div>
    """
)


risk = data[
    (data["Days_Since_Last_Activity"] > 45) &
    (data["Customer_Satisfaction"] < 3)
]


with st.container(border=True):

    st.dataframe(
        risk,
        width="stretch",
        hide_index=True
    )

    st.write(
        f"**Total High Risk Customers:** {len(risk)}"
    )


# ============================================================
# TOP 10 LEAST ACTIVE CUSTOMERS
# ============================================================

st.html(
    """
    <div class="cp-section">
        🕒 Least Active Customers
    </div>
    """
)


least = (
    data.sort_values(
        "Days_Since_Last_Activity",
        ascending=False
    )
    .head(10)
)


with st.container(border=True):

    st.dataframe(
        least,
        width="stretch",
        hide_index=True
    )

# ============================================================
# CUSTOMER BEHAVIOR INSIGHTS
# ============================================================

st.html(
    """
    <div class="cp-section">
        📌 Customer Behavior Insights
    </div>
    """
)

# ------------------------------------------------------------
# CUSTOMER BEHAVIOR CALCULATIONS
# ------------------------------------------------------------

# Customers inactive for more than 30 days
inactive_30 = data[
    data["Days_Since_Last_Activity"] > 30
]

# Customers with low satisfaction
low_satisfaction = data[
    data["Customer_Satisfaction"] < 3
]

# Existing high-risk definition
high_risk_count = len(risk)

# Average engagement rate
average_engagement = data["Engagement_Rate"].mean()

# Average watch time for active customers
active_data = data[
    data["Churn_Status"] == "No"
]

# Average watch time for churned customers
churned_data = data[
    data["Churn_Status"] == "Yes"
]

if not active_data.empty:
    active_watch_time = active_data["Daily_Watch_Time"].mean()
else:
    active_watch_time = 0

if not churned_data.empty:
    churned_watch_time = churned_data["Daily_Watch_Time"].mean()
else:
    churned_watch_time = 0


# ------------------------------------------------------------
# INSIGHT CARDS
# ------------------------------------------------------------

insight1, insight2, insight3 = st.columns(3)


with insight1:

    st.html(
        f"""
        <div class="cp-kpi">

            <div class="cp-kpi-label">
                🕒 Inactive Customers
            </div>

            <div class="cp-kpi-value">
                {len(inactive_30):,}
            </div>

            <div class="cp-kpi-info">
                Inactive for more than 30 days
            </div>

        </div>
        """
    )


with insight2:

    st.html(
        f"""
        <div class="cp-kpi">

            <div class="cp-kpi-label">
                ⭐ Low Satisfaction
            </div>

            <div class="cp-kpi-value">
                {len(low_satisfaction):,}
            </div>

            <div class="cp-kpi-info">
                Satisfaction score below 3
            </div>

        </div>
        """
    )


with insight3:

    st.html(
        f"""
        <div class="cp-kpi">

            <div class="cp-kpi-label">
                ⚠️ High Risk Customers
            </div>

            <div class="cp-kpi-value">
                {high_risk_count:,}
            </div>

            <div class="cp-kpi-info">
                Based on inactivity and satisfaction
            </div>

        </div>
        """
    )


# ------------------------------------------------------------
# CUSTOMER BEHAVIOR SUMMARY
# ------------------------------------------------------------

st.html(
    """
    <div style="margin-top: 22px;">
    </div>
    """
)

st.html(
    f"""
    <div class="cp-recommendation">

        <strong>📊 Customer Engagement</strong>
        <br><br>

        Average engagement rate across customers:
        <strong>{average_engagement:.1f}</strong>

        <br><br>

        Active customers watch an average of
        <strong>{active_watch_time:.2f} hours/day</strong>,
        while churned customers watch an average of
        <strong>{churned_watch_time:.2f} hours/day</strong>.

    </div>
    """
)
