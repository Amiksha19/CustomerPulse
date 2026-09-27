import streamlit as st
import plotly.express as px
from database.db_connection import run_query

st.set_page_config(
    page_title="SQL Analysis",
    page_icon="🗄️",
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
       SECTION HEADING
    ======================================================== */

    .cp-section {
        color: #56327F;
        font-size: 22px;
        font-weight: 750;

        margin-top: 20px;
        margin-bottom: 18px;
    }


    /* ========================================================
       ANALYSIS SELECTOR CARD
    ======================================================== */

    .cp-selector-card {
        background: #EDE3F8;
        border: 1px solid #D8C5ED;
        border-radius: 18px;

        padding: 18px 22px;

        margin-bottom: 25px;

        box-shadow:
            0 5px 18px rgba(91, 58, 142, 0.07);
    }

    .cp-selector-label {
        color: #56327F;
        font-size: 15px;
        font-weight: 700;

        margin-bottom: 8px;
    }


    /* ========================================================
       CONTENT CARD
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
       METRIC CARD
    ======================================================== */

    .cp-metric-card {
        background: #EDE3F8;
        border: 1px solid #D8C5ED;
        border-radius: 18px;

        padding: 25px;

        min-height: 145px;

        box-shadow:
            0 5px 18px rgba(91, 58, 142, 0.07);
    }

    .cp-metric-label {
        color: #766783;
        font-size: 14px;
        font-weight: 600;

        margin-bottom: 12px;
    }

    .cp-metric-value {
        color: #4B286F;
        font-size: 32px;
        font-weight: 800;
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
       SELECTBOX
    ======================================================== */

    div[data-baseweb="select"] > div {
        background-color: #F8F5FC !important;
        border: 1px solid #D8C5ED !important;
        border-radius: 12px !important;
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
    div[data-baseweb="select"],
    div[data-baseweb="select"] *,
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
    .cp-selector-label,
    .cp-metric-label,
    .cp-metric-value,
    .cp-footer-title,
    .cp-footer-text {
        font-family: 'Patrick Hand', sans-serif !important;
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
            🗄️ SQL Business Analysis
        </div>

        <div class="cp-header-subtitle">
            Explore business insights directly from the MySQL database.
        </div>

    </div>
    """
)


# ============================================================
# QUERY SELECTION
# ============================================================

st.html(
    """
    <div class="cp-section">
        🔍 Select Analysis
    </div>
    """
)


st.html(
    """
    <div class="cp-selector-card">

        <div class="cp-selector-label">
            Choose an analysis to explore
        </div>

    </div>
    """
)


option = st.selectbox(
    "Select Analysis",
    (
        "Subscription Plan Distribution",
        "Churn Distribution",
        "Region Distribution",
        "Device Distribution",
        "Average Customer Satisfaction",
        "Average Watch Time"
    ),
    label_visibility="collapsed"
)


# ============================================================
# SUBSCRIPTION PLAN
# ============================================================

if option == "Subscription Plan Distribution":

    st.html(
        """
        <div class="cp-section">
            📊 Subscription Plan Distribution
        </div>
        """
    )

    df = run_query("""
        SELECT
            Subscription_Plan,
            COUNT(*) AS Customers
        FROM customer_data
        GROUP BY Subscription_Plan
    """)

    # --------------------------------------------------------
    # TABLE
    # --------------------------------------------------------

    with st.container(border=True):

        st.dataframe(
            df,
            width="stretch",
            hide_index=True
        )

    # --------------------------------------------------------
    # CHART
    # --------------------------------------------------------

    fig = px.bar(
        df,
        x="Subscription_Plan",
        y="Customers",
        text="Customers",
        title="Subscription Plan Distribution"
    )

    fig.update_traces(
        textposition="outside",
        marker_color="#B98EDC"
    )

    fig.update_layout(
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
        ),

        showlegend=False
    )

    with st.container(border=True):

        st.plotly_chart(
            fig,
            width="stretch",
            config={
                "displayModeBar": False
            }
        )


# ============================================================
# CHURN DISTRIBUTION
# ============================================================

elif option == "Churn Distribution":

    st.html(
        """
        <div class="cp-section">
            📉 Churn Distribution
        </div>
        """
    )

    df = run_query("""
        SELECT
            Churn,
            COUNT(*) AS Customers
        FROM customer_data
        GROUP BY Churn
    """)

    # --------------------------------------------------------
    # TABLE
    # --------------------------------------------------------

    with st.container(border=True):

        st.dataframe(
            df,
            width="stretch",
            hide_index=True
        )

    # --------------------------------------------------------
    # CHART
    # --------------------------------------------------------

    fig = px.pie(
        df,
        names="Churn",
        values="Customers",
        hole=0.45,
        title="Customer Churn"
    )

    fig.update_layout(
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
            fig,
            width="stretch",
            config={
                "displayModeBar": False
            }
        )


# ============================================================
# REGION DISTRIBUTION
# ============================================================

elif option == "Region Distribution":

    st.html(
        """
        <div class="cp-section">
            🌍 Region Distribution
        </div>
        """
    )

    df = run_query("""
        SELECT
            Region,
            COUNT(*) AS Customers
        FROM customer_data
        GROUP BY Region
    """)

    # --------------------------------------------------------
    # TABLE
    # --------------------------------------------------------

    with st.container(border=True):

        st.dataframe(
            df,
            width="stretch",
            hide_index=True
        )

    # --------------------------------------------------------
    # CHART
    # --------------------------------------------------------

    fig = px.bar(
        df,
        x="Region",
        y="Customers",
        text="Customers",
        title="Customers by Region"
    )

    fig.update_traces(
        textposition="outside",
        marker_color="#B98EDC"
    )

    fig.update_layout(
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
        ),

        showlegend=False
    )

    with st.container(border=True):

        st.plotly_chart(
            fig,
            width="stretch",
            config={
                "displayModeBar": False
            }
        )


# ============================================================
# DEVICE DISTRIBUTION
# ============================================================

elif option == "Device Distribution":

    st.html(
        """
        <div class="cp-section">
            📱 Device Distribution
        </div>
        """
    )

    df = run_query("""
        SELECT
            Device,
            COUNT(*) AS Customers
        FROM customer_data
        GROUP BY Device
    """)

    # --------------------------------------------------------
    # TABLE
    # --------------------------------------------------------

    with st.container(border=True):

        st.dataframe(
            df,
            width="stretch",
            hide_index=True
        )

    # --------------------------------------------------------
    # CHART
    # --------------------------------------------------------

    fig = px.bar(
        df,
        x="Device",
        y="Customers",
        text="Customers",
        title="Device Usage"
    )

    fig.update_traces(
        textposition="outside",
        marker_color="#B98EDC"
    )

    fig.update_layout(
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
        ),

        showlegend=False
    )

    with st.container(border=True):

        st.plotly_chart(
            fig,
            width="stretch",
            config={
                "displayModeBar": False
            }
        )


# ============================================================
# CUSTOMER SATISFACTION
# ============================================================

elif option == "Average Customer Satisfaction":

    st.html(
        """
        <div class="cp-section">
            ⭐ Average Customer Satisfaction
        </div>
        """
    )

    df = run_query("""
        SELECT
            AVG(Customer_Satisfaction) AS Average_Satisfaction
        FROM customer_data
    """)

    value = df.iloc[0]["Average_Satisfaction"]


    if value is not None:

        display_value = f"{float(value):.2f}"

    else:

        display_value = "N/A"


    st.html(
        f"""
        <div class="cp-metric-card">

            <div class="cp-metric-label">
                ⭐ Average Customer Satisfaction
            </div>

            <div class="cp-metric-value">
                {display_value}
            </div>

        </div>
        """
    )


# ============================================================
# WATCH TIME
# ============================================================

elif option == "Average Watch Time":

    st.html(
        """
        <div class="cp-section">
            ⏱️ Average Watch Time
        </div>
        """
    )

    df = run_query("""
        SELECT
            AVG(Daily_Watch_Time) AS Average_Watch_Time
        FROM customer_data
    """)

    value = df.iloc[0]["Average_Watch_Time"]


    if value is not None:

        display_value = f"{float(value):.2f}"

    else:

        display_value = "N/A"


    st.html(
        f"""
        <div class="cp-metric-card">

            <div class="cp-metric-label">
                ⏱️ Average Daily Watch Time
            </div>

            <div class="cp-metric-value">
                {display_value}
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