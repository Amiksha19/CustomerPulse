import streamlit as st
import pandas as pd
import mysql.connector
from io import BytesIO
from datetime import datetime

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_CENTER
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os


# ============================================================
# PAGE CONFIG
# ============================================================
st.set_page_config(
    page_title="Retention Action Center",
    page_icon="🎯",
    layout="wide"
)


# ============================================================
# CUSTOMERPULSE UI
# ============================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Patrick+Hand&display=swap');

/* ----------------------------------------------------------
   Main application font
   Do NOT apply Patrick Hand to every internal Streamlit
   element because that breaks Streamlit Material icons.
---------------------------------------------------------- */
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

.stApp {
    background: #F8F5FC;
    color: #56327F;
}

.block-container {
    max-width: 1200px;
    padding-top: 1.2rem;
    padding-bottom: 2rem;
}


/* ==========================================================
   HEADER
========================================================== */
.cp-header {
    background: #EDE3F8;
    border: 1px solid #D8C5ED;
    border-radius: 22px;
    padding: 24px 30px;
    margin-bottom: 28px;
    box-shadow: 0 5px 18px rgba(86, 50, 127, 0.07);
}

.cp-header h1 {
    color: #4B286F;
    font-size: 34px;
    margin: 0;
    font-weight: 600;
}


/* ==========================================================
   SECTION HEADINGS
========================================================== */
.section {
    color: #4B286F;
    font-size: 25px;
    font-weight: 600;
    margin: 25px 0 12px;
}


/* ==========================================================
   KPI CARDS
========================================================== */
.kpi {
    background: #EDE3F8;
    border: 1px solid #D8C5ED;
    border-radius: 18px;
    padding: 17px;
    min-height: 105px;
    box-shadow: 0 4px 14px rgba(86, 50, 127, 0.05);
}

.kpi-label {
    color: #78698A;
    font-size: 16px;
}

.kpi-value {
    color: #4B286F;
    font-size: 31px;
    font-weight: 600;
    margin-top: 3px;
}


/* ==========================================================
   CARDS
========================================================== */
.card,
.report {
    background: #EDE3F8;
    border: 1px solid #D8C5ED;
    border-radius: 18px;
    padding: 18px;
    margin: 12px 0;
    box-shadow: 0 4px 14px rgba(86, 50, 127, 0.04);
}

.card h3,
.report h3 {
    color: #4B286F;
    margin-top: 0;
    font-size: 21px;
}

.card p,
.report p {
    color: #56327F;
    font-size: 16px;
    margin: 5px 0;
}


/* ==========================================================
   LABELS
========================================================== */
label,
.stSelectbox label,
.stTextArea label {
    color: #56327F !important;
    font-family: 'Patrick Hand', sans-serif !important;
    font-size: 16px !important;
}


/* ==========================================================
   SELECT BOXES
   Keep Streamlit's internal icon font untouched.
========================================================== */
div[data-baseweb="select"] > div {
    border-radius: 12px !important;
    border-color: #D8C5ED !important;
    color: #56327F !important;
}

div[data-baseweb="select"] * {
    font-family: 'Patrick Hand', sans-serif !important;
}


/* ==========================================================
   TEXT AREA
========================================================== */
.stTextArea textarea {
    border-radius: 12px !important;
    border-color: #D8C5ED !important;
    font-family: 'Patrick Hand', sans-serif !important;
    color: #56327F !important;
    font-size: 16px !important;
}


/* ==========================================================
   BUTTONS
========================================================== */
.stButton > button,
.stDownloadButton > button {
    width: 100%;
    border-radius: 12px;
    border: 1px solid #D8C5ED;
    background: #EDE3F8;
    color: #56327F;
    font-family: 'Patrick Hand', sans-serif !important;
    font-size: 16px !important;
}

.stButton > button:hover,
.stDownloadButton > button:hover {
    border-color: #B98EDC;
    color: #4B286F;
}


/* ==========================================================
   DATAFRAME
========================================================== */
.stDataFrame {
    border-radius: 14px;
}


/* ==========================================================
   ALERTS
========================================================== */
div[data-testid="stAlert"] {
    border-radius: 12px;
}


/* ==========================================================
   FOOTER
========================================================== */
.footer {
    background: #EDE3F8;
    border: 1px solid #D8C5ED;
    border-radius: 20px;
    padding: 20px;
    text-align: center;
    margin-top: 35px;
}

.footer-title {
    color: #4B286F;
    font-size: 22px;
}

.footer-subtitle {
    color: #78698A;
    font-size: 15px;
    margin-top: 5px;
}

hr {
    border-color: #D8C5ED !important;
}
</style>
""", unsafe_allow_html=True)


# ============================================================
# DATABASE
# ============================================================
def get_connection():
    return mysql.connector.connect(
        host=st.secrets["mysql"]["host"],
        user=st.secrets["mysql"]["user"],
        password=st.secrets["mysql"]["password"],
        database=st.secrets["mysql"]["database"]
    )

def load_data():
    connection = get_connection()
    cursor = connection.cursor(dictionary=True)

    cursor.execute("""
        SELECT *
        FROM customer_data
        ORDER BY Customer_ID
    """)

    rows = cursor.fetchall()

    cursor.close()
    connection.close()

    return pd.DataFrame(rows)


# ============================================================
# DATA HELPERS
# ============================================================
def normalize_churn(value):
    return (
        "Yes"
        if str(value).strip().lower()
        in ["1", "yes", "y", "true", "churn", "churned"]
        else "No"
    )


# ============================================================
# RETENTION SITUATIONS
# ============================================================
SITUATIONS = {
    "Needs Attention": {
        "title": "Low Satisfaction + Long Inactivity",
        "action": "Contact the customer and encourage re-engagement.",
        "Email": (
            "Hi, we noticed that you have not been as active recently. "
            "We would value your feedback and would be happy to help "
            "with any concerns you may have."
        ),
        "WhatsApp": (
            "Hi, we noticed you have not been as active recently. "
            "We would love to hear your feedback and help improve your experience."
        ),
        "SMS": (
            "Hi, we noticed you have not been active recently. "
            "We would love to hear your feedback and help with any concerns."
        )
    },

    "Low Engagement": {
        "title": "Low Customer Engagement",
        "action": "Send relevant content and a re-engagement communication.",
        "Email": (
            "Hi, we wanted to share some content that you may enjoy. "
            "We hope you will come back and discover something new with us."
        ),
        "WhatsApp": (
            "Hi, we have some content you may enjoy. "
            "Come back and discover something new with us."
        ),
        "SMS": (
            "Hi, discover something new with us. "
            "We have content you may enjoy."
        )
    },

    "Support Concern": {
        "title": "High Support Activity",
        "action": "Contact the customer and resolve their support concerns.",
        "Email": (
            "Hi, we noticed that you have recently contacted our support "
            "team several times. We would like to make sure your concerns "
            "are properly resolved. Please let us know how we can help."
        ),
        "WhatsApp": (
            "Hi, we noticed your recent support activity. "
            "We would like to make sure your concerns are properly resolved. "
            "Please let us know how we can help."
        ),
        "SMS": (
            "Hi, we noticed your recent support activity. "
            "Please let us know if there is anything we can help resolve."
        )
    },

    "Churned Customers": {
        "title": "Customer Marked as Churned",
        "action": "Send a re-engagement communication and suitable retention offer.",
        "Email": (
            "Hi, we would love to welcome you back. "
            "We value your experience with us and would be happy to help "
            "you find an option that works for you."
        ),
        "WhatsApp": (
            "Hi, we would love to welcome you back. "
            "Let us know how we can help you get started again."
        ),
        "SMS": (
            "Hi, we would love to welcome you back. "
            "Contact us to explore what is available for you."
        )
    }
}


# ============================================================
# PDF FONT - TIMES NEW ROMAN
# ============================================================

times_new_roman = r"C:\Windows\Fonts\times.ttf"
times_new_roman_bold = r"C:\Windows\Fonts\timesbd.ttf"

if os.path.exists(times_new_roman):
    pdfmetrics.registerFont(
        TTFont("TimesNewRoman", times_new_roman)
    )

if os.path.exists(times_new_roman_bold):
    pdfmetrics.registerFont(
        TTFont("TimesNewRoman-Bold", times_new_roman_bold)
    )


# ============================================================
# PDF REPORT
# ============================================================
def make_report(df, group, plan, region, situation, message):
    buffer = BytesIO()

    document = SimpleDocTemplate(
        buffer,
        pagesize=landscape(A4),
        rightMargin=28,
        leftMargin=28,
        topMargin=28,
        bottomMargin=28
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        "ReportTitle",
        parent=styles["Title"],
        fontName="TimesNewRoman-Bold",
        fontSize=21,
        textColor=colors.HexColor("#4B286F"),
        alignment=TA_CENTER,
        spaceAfter=8
    )

    heading_style = ParagraphStyle(
        "ReportHeading",
        parent=styles["Heading2"],
        fontName="TimesNewRoman-Bold",
        fontSize=14,
        textColor=colors.HexColor("#4B286F"),
        spaceBefore=8,
        spaceAfter=7
    )

    body_style = ParagraphStyle(
        "ReportBody",
        parent=styles["Normal"],
        fontName="TimesNewRoman",
        fontSize=9,
        leading=13,
        textColor=colors.HexColor("#56327F")
    )

    story = [
        Paragraph(
            "CustomerPulse - Retention Action Report",
            title_style
        ),
        Paragraph(
            datetime.now().strftime(
                "Generated: %d %B %Y, %I:%M %p"
            ),
            body_style
        ),
        Spacer(1, 12),
        Paragraph("Report Summary", heading_style)
    ]

    summary = [
        ["Customer Group", group],
        ["Subscription Plan", plan],
        ["Region", region],
        ["Customers", str(len(df))],
        ["Situation", situation["title"]],
        ["Recommended Action", situation["action"]]
    ]

    summary_table = Table(
        summary,
        colWidths=[150, 540]
    )

    summary_table.setStyle(
        TableStyle([
            (
                "BACKGROUND",
                (0, 0),
                (0, -1),
                colors.HexColor("#EDE3F8")
            ),
            (
                "BACKGROUND",
                (1, 0),
                (1, -1),
                colors.HexColor("#FAF8FD")
            ),
            (
                "GRID",
                (0, 0),
                (-1, -1),
                0.4,
                colors.HexColor("#D8C5ED")
            ),
            (
                "FONTNAME",
                (0, 0),
                (-1, -1),
                "TimesNewRoman"
            ),
            (
                "FONTSIZE",
                (0, 0),
                (-1, -1),
                9
            ),
            (
                "TEXTCOLOR",
                (0, 0),
                (-1, -1),
                colors.HexColor("#56327F")
            ),
            (
                "VALIGN",
                (0, 0),
                (-1, -1),
                "TOP"
            ),
            (
                "PADDING",
                (0, 0),
                (-1, -1),
                6
            )
        ])
    )

    story.extend([
        summary_table,
        Spacer(1, 12),
        Paragraph("Review Message", heading_style),
        Paragraph(
            message.replace("\n", "<br/>"),
            body_style
        ),
        Spacer(1, 12),
        Paragraph("Customers", heading_style)
    ])

    report_columns = [
        "Customer_ID",
        "Subscription_Plan",
        "Region",
        "Customer_Satisfaction",
        "Daily_Watch_Time",
        "Engagement_Rate",
        "Support_Queries",
        "Days_Since_Last_Activity",
        "Churn_Status"
    ]

    report_columns = [
        column
        for column in report_columns
        if column in df.columns
    ]

    table_rows = [
        [column.replace("_", " ") for column in report_columns]
    ]

    for _, row in df[report_columns].iterrows():
        table_rows.append(
            [str(row[column]) for column in report_columns]
        )

    customer_table = Table(
        table_rows,
        repeatRows=1
    )

    customer_table.setStyle(
        TableStyle([
            (
                "BACKGROUND",
                (0, 0),
                (-1, 0),
                colors.HexColor("#EDE3F8")
            ),
            (
                "TEXTCOLOR",
                (0, 0),
                (-1, 0),
                colors.HexColor("#4B286F")
            ),
            (
                "BACKGROUND",
                (0, 1),
                (-1, -1),
                colors.HexColor("#FAF8FD")
            ),
            (
                "TEXTCOLOR",
                (0, 1),
                (-1, -1),
                colors.HexColor("#56327F")
            ),
            (
                "GRID",
                (0, 0),
                (-1, -1),
                0.35,
                colors.HexColor("#D8C5ED")
            ),
            (
                "FONTNAME",
                (0, 0),
                (-1, -1),
                "TimesNewRoman"
            ),
            (
                "FONTSIZE",
                (0, 0),
                (-1, -1),
                7
            ),
            (
                "VALIGN",
                (0, 0),
                (-1, -1),
                "MIDDLE"
            ),
            (
                "PADDING",
                (0, 0),
                (-1, -1),
                4
            )
        ])
    )

    story.append(customer_table)

    document.build(story)

    buffer.seek(0)
    return buffer.getvalue()


# ============================================================
# HEADER
# ============================================================
st.markdown(
    """
    <div class="cp-header">
        <h1>🎯 Retention Action Center</h1>
    </div>
    """,
    unsafe_allow_html=True
)


# ============================================================
# LOAD DATABASE DATA
# ============================================================
try:
    data = load_data()

except Exception as e:
    st.error(f"Unable to load customer data: {e}")
    st.stop()


if data.empty:
    st.info("No customer data is available.")
    st.stop()


# ============================================================
# PREPARE DATA
# ============================================================
data["Churn_Status"] = data["Churn"].apply(normalize_churn)

for column in [
    "Customer_Satisfaction",
    "Daily_Watch_Time",
    "Engagement_Rate",
    "Support_Queries",
    "Days_Since_Last_Activity",
    "Age",
    "Monthly_Income"
]:
    if column in data.columns:
        data[column] = pd.to_numeric(
            data[column],
            errors="coerce"
        )


# ============================================================
# RETENTION OVERVIEW
# ============================================================
st.markdown(
    '<div class="section">📌 Retention Overview</div>',
    unsafe_allow_html=True
)

attention = data[
    (data["Days_Since_Last_Activity"] > 45) &
    (data["Customer_Satisfaction"] < 3)
]

low_engagement = data[
    data["Engagement_Rate"] < 30
]

support_concern = data[
    data["Support_Queries"] >= 5
]

churned = data[
    data["Churn_Status"] == "Yes"
]

kpi_items = [
    ("⚠️ Attention", len(attention)),
    ("📉 Low Engagement", len(low_engagement)),
    ("🛠 Support Concern", len(support_concern)),
    ("🔴 Churned", len(churned))
]

kpi_columns = st.columns(4)

for column, (label, value) in zip(kpi_columns, kpi_items):
    with column:
        st.markdown(
            f"""
            <div class="kpi">
                <div class="kpi-label">{label}</div>
                <div class="kpi-value">{value}</div>
            </div>
            """,
            unsafe_allow_html=True
        )


# ============================================================
# FIND CUSTOMERS
# ============================================================
st.markdown(
    '<div class="section">🔎 Find Customers</div>',
    unsafe_allow_html=True
)

filter_col1, filter_col2, filter_col3 = st.columns(3)

with filter_col1:
    group = st.selectbox(
        "Customer Group",
        list(SITUATIONS.keys())
    )

with filter_col2:
    plan = st.selectbox(
        "Subscription Plan",
        ["All"]
        + sorted(
            data["Subscription_Plan"]
            .dropna()
            .astype(str)
            .unique()
            .tolist()
        )
    )

with filter_col3:
    region = st.selectbox(
        "Region",
        ["All"]
        + sorted(
            data["Region"]
            .dropna()
            .astype(str)
            .unique()
            .tolist()
        )
    )


# ============================================================
# FILTER CURRENT DATABASE DATA
# ============================================================
filtered = data.copy()

if group == "Needs Attention":
    filtered = filtered[
        (filtered["Days_Since_Last_Activity"] > 45) &
        (filtered["Customer_Satisfaction"] < 3)
    ]

elif group == "Low Engagement":
    filtered = filtered[
        filtered["Engagement_Rate"] < 30
    ]

elif group == "Support Concern":
    filtered = filtered[
        filtered["Support_Queries"] >= 5
    ]

elif group == "Churned Customers":
    filtered = filtered[
        filtered["Churn_Status"] == "Yes"
    ]


if plan != "All":
    filtered = filtered[
        filtered["Subscription_Plan"].astype(str) == plan
    ]


if region != "All":
    filtered = filtered[
        filtered["Region"].astype(str) == region
    ]


filtered = filtered.sort_values(
    "Days_Since_Last_Activity",
    ascending=False
)


# ============================================================
# CUSTOMER TABLE
# ============================================================
st.markdown(
    '<div class="section">👥 Customers Requiring Attention</div>',
    unsafe_allow_html=True
)

if filtered.empty:

    st.info("No customers found.")

else:

    display_columns = [
        "Customer_ID",
        "Subscription_Plan",
        "Region",
        "Customer_Satisfaction",
        "Daily_Watch_Time",
        "Engagement_Rate",
        "Support_Queries",
        "Days_Since_Last_Activity",
        "Churn_Status"
    ]

    display_columns = [
        column
        for column in display_columns
        if column in filtered.columns
    ]

    st.dataframe(
        filtered[display_columns],
        width="stretch",
        hide_index=True
    )

    situation = SITUATIONS[group]


    # ========================================================
    # RETENTION ACTION
    # ========================================================
    st.markdown(
        '<div class="section">🎯 Retention Action</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        f"""
        <div class="card">
            <h3>{situation["title"]}</h3>
            <p><b>Customers:</b> {len(filtered)}</p>
            <p><b>Recommended:</b> {situation["action"]}</p>
        </div>
        """,
        unsafe_allow_html=True
    )


    # ========================================================
    # CUSTOMER MESSAGE
    # ========================================================
    st.markdown(
        '<div class="section">💬 Customer Message</div>',
        unsafe_allow_html=True
    )

    channel = st.selectbox(
        "Channel",
        ["Email", "WhatsApp", "SMS"]
    )

    message = st.text_area(
        "Message",
        value=situation[channel],
        height=125
    )

    st.download_button(
        "📩 Download Message",
        data=message,
        file_name=f"CustomerPulse_{channel}_Message.txt",
        mime="text/plain"
    )


    # ========================================================
    # CUSTOMER REPORT
    # ========================================================
    st.markdown(
        '<div class="section">📄 Customer Report</div>',
        unsafe_allow_html=True
    )

    st.markdown(
        f"""
        <div class="report">
            <h3>Retention Report</h3>
            <p>
                <b>{len(filtered)}</b> customers
                &nbsp;•&nbsp;
                {situation["title"]}
            </p>
        </div>
        """,
        unsafe_allow_html=True
    )

    report = make_report(
        filtered,
        group,
        plan,
        region,
        situation,
        message
    )

    st.download_button(
        "📥 Download Retention Report",
        data=report,
        file_name="CustomerPulse_Retention_Report.pdf",
        mime="application/pdf"
    )


# ============================================================
# FOOTER
# ============================================================
st.markdown(
    """
    <div class="footer">
        <div class="footer-title">💜 CustomerPulse</div>
        <div class="footer-subtitle">
            Customer Churn Analytics & Retention System
        </div>
    </div>
    """,
    unsafe_allow_html=True
)
