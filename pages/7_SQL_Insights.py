import streamlit as st
import pandas as pd
import mysql.connector
import plotly.express as px

st.set_page_config(
    page_title="SQL Insights",
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
       SECTION HEADING
    ======================================================== */

    .cp-section {
        color: #56327F;
        font-size: 22px;
        font-weight: 700;

        margin-top: 20px;
        margin-bottom: 18px;
    }


    /* ========================================================
       KPI CARDS
    ======================================================== */

    .cp-metric-card {
        background: #EDE3F8;
        border: 1px solid #D8C5ED;
        border-radius: 18px;

        padding: 20px;
        min-height: 120px;

        text-align: center;

        box-shadow:
            0 5px 18px rgba(91, 58, 142, 0.07);
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


    /* ========================================================
       CHART CARDS
    ======================================================== */

    .cp-chart-card {
        background: #EDE3F8;
        border: 1px solid #D8C5ED;
        border-radius: 18px;

        padding: 10px;

        box-shadow:
            0 5px 18px rgba(91, 58, 142, 0.07);

        margin-bottom: 22px;
    }


    /* ========================================================
       BUSINESS INSIGHTS CARD
    ======================================================== */

    .cp-insight-card {
        background: #EDE3F8;
        border: 1px solid #D8C5ED;
        border-radius: 18px;

        padding: 25px;

        box-shadow:
            0 5px 18px rgba(91, 58, 142, 0.07);
    }

    .cp-insight-title {
        color: #56327F;
        font-size: 22px;
        font-weight: 800;
        margin-bottom: 15px;
    }

    .cp-insight-text {
        color: #78698A;
        font-size: 16px;
        line-height: 1.7;
    }

    .cp-insight-text strong {
        color: #4B286F;
    }


    /* ========================================================
       ALERTS
    ======================================================== */

    div[data-testid="stAlert"] {
        border-radius: 15px !important;
        border: 1px solid #D8C5ED !important;
    }

    div[data-testid="stAlert"] * {
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


    /* ========================================================
       FOOTER
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
# PAGE HEADER
# ============================================================

st.html(
    """
    <div class="cp-header-card">

        <div class="cp-header-title">
            📊 SQL Business Insights
        </div>

        <div class="cp-header-subtitle">
            Business insights generated directly from the
            MySQL database.
        </div>

    </div>
    """
)


# ============================================================
# MYSQL CONNECTION
# ============================================================

conn = mysql.connector.connect(
    host=st.secrets["mysql"]["host"],
    user=st.secrets["mysql"]["user"],
    password=st.secrets["mysql"]["password"],
    database=st.secrets["mysql"]["database"]
)

cursor = conn.cursor()

query = "SELECT * FROM customer_data"

cursor.execute(query)

rows = cursor.fetchall()

columns = [
    description[0]
    for description in cursor.description
]

cursor.close()
conn.close()

df = pd.DataFrame(
    rows,
    columns=columns
)


# ============================================================
# CHECK DATABASE DATA
# ============================================================

if df.empty:

    st.info(
        "No customer data is available in the database yet."
    )

    st.stop()


# ============================================================
# CONVERT CHURN COLUMN
# ============================================================

df["Churn"] = (
    df["Churn"]
    .astype(str)
    .str.strip()
    .str.lower()
    .map(
        {
            "yes": 1,
            "no": 0,
            "1": 1,
            "0": 0,
            "true": 1,
            "false": 0
        }
    )
)

df["Churn"] = pd.to_numeric(
    df["Churn"],
    errors="coerce"
)

df = df.dropna(
    subset=["Churn"]
)


# ============================================================
# KPI SECTION
# ============================================================

st.html(
    """
    <div class="cp-section">
        📌 Key Performance Indicators
    </div>
    """
)

churn_rate = (
    df["Churn"].mean() * 100
)

col1, col2, col3, col4 = st.columns(4)


with col1:

    st.html(
        f"""
        <div class="cp-metric-card">

            <div class="cp-metric-label">
                Total Customers
            </div>

            <div class="cp-metric-value">
                {len(df)}
            </div>

        </div>
        """
    )


with col2:

    st.html(
        f"""
        <div class="cp-metric-card">

            <div class="cp-metric-label">
                Overall Churn
            </div>

            <div class="cp-metric-value">
                {churn_rate:.2f}%
            </div>

        </div>
        """
    )


with col3:

    st.html(
        f"""
        <div class="cp-metric-card">

            <div class="cp-metric-label">
                Average Age
            </div>

            <div class="cp-metric-value">
                {df['Age'].mean():.1f}
            </div>

        </div>
        """
    )


with col4:

    st.html(
        f"""
        <div class="cp-metric-card">

            <div class="cp-metric-label">
                Average Watch Time
            </div>

            <div class="cp-metric-value">
                {df['Daily_Watch_Time'].mean():.2f} hrs
            </div>

        </div>
        """
    )


# ============================================================
# CHURN BY SUBSCRIPTION PLAN
# ============================================================

st.html(
    '<div class="cp-divider"></div>'
)

st.html(
    """
    <div class="cp-section">
        📈 Churn by Subscription Plan
    </div>
    """
)

plan = (
    df.groupby("Subscription_Plan")["Churn"]
    .mean()
    .reset_index()
)

plan["Churn"] = plan["Churn"] * 100


with st.container(border=True):

    fig = px.bar(
        plan,
        x="Subscription_Plan",
        y="Churn",
        color="Subscription_Plan",
        text="Churn",
        title="Churn Rate by Subscription Plan"
    )

    fig.update_traces(
        texttemplate="%{text:.1f}%",
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
        )
    )

    st.plotly_chart(
        fig,
        width="stretch"
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

device = (
    df["Device"]
    .value_counts()
    .reset_index()
)

device.columns = [
    "Device",
    "Customers"
]


with st.container(border=True):

    fig = px.pie(
        device,
        names="Device",
        values="Customers",
        hole=0.45,
        title="Customer Device Distribution"
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
        )
    )

    st.plotly_chart(
        fig,
        width="stretch"
    )


# ============================================================
# GENRE PREFERENCE
# ============================================================

st.html(
    """
    <div class="cp-section">
        🎬 Favourite Genres
    </div>
    """
)

genre = (
    df["Genre"]
    .value_counts()
    .reset_index()
)

genre.columns = [
    "Genre",
    "Customers"
]


with st.container(border=True):

    fig = px.bar(
        genre,
        x="Genre",
        y="Customers",
        color="Genre",
        text="Customers",
        title="Favourite Genres"
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
        )
    )

    st.plotly_chart(
        fig,
        width="stretch"
    )


# ============================================================
# REGION DISTRIBUTION
# ============================================================

st.html(
    """
    <div class="cp-section">
        🌍 Region Distribution
    </div>
    """
)

region = (
    df["Region"]
    .value_counts()
    .reset_index()
)

region.columns = [
    "Region",
    "Customers"
]


with st.container(border=True):

    fig = px.bar(
        region,
        x="Region",
        y="Customers",
        color="Region",
        text="Customers",
        title="Customers by Region"
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
        )
    )

    st.plotly_chart(
        fig,
        width="stretch"
    )


# ============================================================
# BUSINESS INSIGHTS
# ============================================================

st.html(
    '<div class="cp-divider"></div>'
)

st.html(
    """
    <div class="cp-section">
        💡 Business Insights
    </div>
    """
)


highest_plan = (
    plan
    .sort_values(
        "Churn",
        ascending=False
    )
    .iloc[0]["Subscription_Plan"]
)

highest_region = (
    region
    .sort_values(
        "Customers",
        ascending=False
    )
    .iloc[0]["Region"]
)

top_genre = (
    genre
    .sort_values(
        "Customers",
        ascending=False
    )
    .iloc[0]["Genre"]
)


st.html(
    f"""
    <div class="cp-insight-card">

        <div class="cp-insight-title">
            📌 Business Summary
        </div>

        <div class="cp-insight-text">

            ✅ <strong>
            Highest churn occurs in the {highest_plan} Plan
            </strong>

            <br><br>

            ✅ <strong>
            Most customers belong to {highest_region}
            </strong>

            <br><br>

            ✅ <strong>
            Most preferred genre is {top_genre}
            </strong>

            <br><br>

            ✅ <strong>
            Overall churn rate is {churn_rate:.2f}%
            </strong>

            <br><br>

            <strong>Recommendations</strong>

            <br><br>

            • Improve retention strategies for customers on the
            <strong>{highest_plan} Plan</strong>.

            <br>

            • Create personalized content around
            <strong>{top_genre}</strong> since it has the highest
            customer count.

            <br>

            • Focus marketing campaigns in
            <strong>{highest_region}</strong> where the customer
            base is largest.

            <br>

            • Launch loyalty offers for inactive users to reduce
            the <strong>{churn_rate:.2f}% churn rate</strong>.

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