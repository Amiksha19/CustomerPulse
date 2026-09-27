import streamlit as st

st.set_page_config(
    page_title="CustomerPulse",
    page_icon="📊",
    layout="wide"
)

# ============================================================
# CUSTOMERPULSE NAVIGATION
# ============================================================

dashboard = st.Page(
    "pages/2_Dashboard.py",
    title="Dashboard",
    icon="📊",
    default=True
)

predict_churn = st.Page(
    "pages/1_Predict_Churn.py",
    title="Predict Churn",
    icon="🔮"
)

sql_analysis = st.Page(
    "pages/3_SQL_Analysis.py",
    title="SQL Analysis",
    icon="📈"
)

customer_insights = st.Page(
    "pages/4_Customer_Insights.py",
    title="Customer Insights",
    icon="👥"
)

retention_system = st.Page(
    "pages/5_Retention_System.py",
    title="Retention System",
    icon="🎯"
)

sql_insights = st.Page(
    "pages/7_SQL_Insights.py",
    title="SQL Insights",
    icon="📊"
)

pg = st.navigation([
    dashboard,
    predict_churn,
    sql_analysis,
    customer_insights,
    retention_system,
    sql_insights
])

pg.run()