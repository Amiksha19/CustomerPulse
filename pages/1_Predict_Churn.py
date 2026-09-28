import streamlit as st
import pandas as pd
import mysql.connector
import os
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from utils.recommendation import get_recommendations
from utils.prediction import (
    get_model,
    get_features,
    get_label_encoders
)


# ============================================================
# PDF FONT - TIMES NEW ROMAN
# ============================================================

TIMES_NEW_ROMAN = r"C:\Windows\Fonts\times.ttf"
TIMES_NEW_ROMAN_BOLD = r"C:\Windows\Fonts\timesbd.ttf"

if os.path.exists(TIMES_NEW_ROMAN):
    if "TimesNewRoman" not in pdfmetrics.getRegisteredFontNames():
        pdfmetrics.registerFont(
            TTFont("TimesNewRoman", TIMES_NEW_ROMAN)
        )

if os.path.exists(TIMES_NEW_ROMAN_BOLD):
    if "TimesNewRoman-Bold" not in pdfmetrics.getRegisteredFontNames():
        pdfmetrics.registerFont(
            TTFont("TimesNewRoman-Bold", TIMES_NEW_ROMAN_BOLD)
        )




# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Predict Churn - CustomerPulse",
    page_icon="🎯",
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
    .stApp { background: #F8F5FC; }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 3rem;
        padding-left: 3rem;
        padding-right: 3rem;
        max-width: 1250px;
    }

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
        font-size: 15px;
        margin-top: 7px;
        line-height: 1.5;
    }

    .cp-section {
        color: #56327F;
        font-size: 22px;
        font-weight: 700;
        margin-top: 20px;
        margin-bottom: 18px;
    }

    div[data-testid="stVerticalBlockBorderWrapper"] {
        background: #EDE3F8 !important;
        border: 1px solid #D8C5ED !important;
        border-radius: 18px !important;
        box-shadow: 0 5px 18px rgba(91, 58, 142, 0.07);
    }

    [data-testid="stWidgetLabel"] p,
    [data-testid="stWidgetLabel"] label {
        color: #56327F !important;
        font-size: 15px !important;
        font-weight: 600 !important;
    }

    .stTextInput input,
    .stTextArea textarea,
    .stNumberInput input {
        background: #FFFFFF !important;
        color: #56327F !important;
        border: 1px solid #D8C5ED !important;
        border-radius: 12px !important;
    }

    div[data-baseweb="select"] > div {
        background: #FFFFFF !important;
        border: 1px solid #D8C5ED !important;
        border-radius: 12px !important;
    }

    div[data-baseweb="select"] * {
        color: #56327F !important;
        font-family: 'Patrick Hand', sans-serif !important;
    }

    .stButton > button {
        background: #EDE3F8 !important;
        color: #56327F !important;
        border: 1px solid #D1BCE8 !important;
        border-radius: 12px !important;
        font-size: 15px !important;
        font-weight: 700 !important;
        padding: 10px 14px !important;
        transition: 0.2s ease;
    }

    .stButton > button:hover {
        background: #E3D5F2 !important;
        border-color: #B99BD8 !important;
        color: #4B286F !important;
        transform: translateY(-2px);
    }

    .stRadio label {
        color: #56327F !important;
        font-weight: 600 !important;
    }

    div[data-testid="stMetric"] {
        background: #EDE3F8;
        border: 1px solid #D8C5ED;
        border-radius: 18px;
        padding: 18px;
        box-shadow: 0 5px 18px rgba(91, 58, 142, 0.07);
    }

    div[data-testid="stMetricLabel"] { color: #78698A !important; }
    div[data-testid="stMetricValue"] { color: #4B286F !important; }

    div[data-testid="stDataFrame"] {
        border-radius: 12px;
        overflow: hidden;
    }

    div[data-testid="stAlert"] {
        border-radius: 15px !important;
        border: 1px solid #D8C5ED !important;
    }

    div[data-testid="stAlert"] * {
        font-family: 'Patrick Hand', sans-serif !important;
    }

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

    header[data-testid="stHeader"] { background: transparent !important; }
    footer { visibility: hidden; }

    </style>
    """,
    unsafe_allow_html=True
)

# ============================================================
# LOAD MODEL
# ============================================================

model = get_model()
features = get_features()
label_encoders = get_label_encoders()


# ============================================================
# MODEL CATEGORY OPTIONS
# ============================================================

def get_category_options(column):
    """
    Get categorical values directly from the trained label encoder.
    This keeps the Streamlit UI exactly aligned with the values
    used by the existing trained model.
    """
    if column not in label_encoders:
        raise ValueError(
            f"No trained encoder found for categorical feature: {column}"
        )

    return [str(value) for value in label_encoders[column].classes_]


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
# LOAD CUSTOMERS
# ============================================================

def load_customers():

    conn = get_connection()
    cursor = conn.cursor()

    query = """
        SELECT *
        FROM customer_data
        ORDER BY Customer_ID
    """

    cursor.execute(query)

    rows = cursor.fetchall()
    columns = [description[0] for description in cursor.description]

    cursor.close()
    conn.close()

    return pd.DataFrame(rows, columns=columns)


customers = load_customers()


# ============================================================
# CUSTOMER ID GENERATION
# ============================================================

def generate_customer_id():

    conn = get_connection()
    cursor = conn.cursor()

    # Create counter table if it doesn't exist
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS customer_id_counter (
            id INT NOT NULL
        )
    """)

    conn.commit()

    # Check counter
    cursor.execute("""
        SELECT id
        FROM customer_id_counter
        LIMIT 1
    """)

    result = cursor.fetchone()

    if result is None:

        # First time creating counter
        cursor.execute("""
            SELECT MAX(
                CAST(
                    SUBSTRING(Customer_ID, 2)
                    AS UNSIGNED
                )
            )
            FROM customer_data
        """)

        max_result = cursor.fetchone()

        if max_result[0] is None:
            next_number = 1
        else:
            next_number = int(max_result[0]) + 1

        cursor.execute(
            """
            INSERT INTO customer_id_counter (id)
            VALUES (%s)
            """,
            (next_number,)
        )

    else:

        next_number = int(result[0]) + 1

        cursor.execute(
            """
            UPDATE customer_id_counter
            SET id = %s
            """,
            (next_number,)
        )

    conn.commit()

    cursor.close()
    conn.close()

    return f"C{next_number:04d}"


# ============================================================
# DELETE CUSTOMER
# ============================================================

def delete_customer(customer_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        """
        DELETE FROM customer_data
        WHERE Customer_ID = %s
        """,
        (customer_id,)
    )

    deleted_rows = cursor.rowcount

    conn.commit()

    cursor.close()
    conn.close()

    return deleted_rows


# ============================================================
# GET MEDIAN INCOME
# ============================================================

def get_median_income():

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT AVG(Monthly_Income)
        FROM customer_data
        WHERE Monthly_Income IS NOT NULL
    """)

    result = cursor.fetchone()

    cursor.close()
    conn.close()

    if result[0] is None:
        return 0.0

    return float(result[0])


# ============================================================
# PREDICTION FUNCTION
# ============================================================

def predict_customer(customer):

    # --------------------------------------------------------
    # Ensure every trained model feature is present
    # --------------------------------------------------------
    missing_features = [
        feature
        for feature in features
        if feature not in customer
    ]

    if missing_features:
        raise ValueError(
            "Missing model features: "
            + ", ".join(missing_features)
        )

    prediction_data = {
        feature: customer[feature]
        for feature in features
    }

    prediction_df = pd.DataFrame(
        [prediction_data],
        columns=features
    )

    # --------------------------------------------------------
    # Handle missing Monthly Income
    # --------------------------------------------------------

    if "Monthly_Income" in prediction_df.columns:

        # Monthly_Income is optional in the UI, so convert it to a
        # numeric dtype before sending the DataFrame to XGBoost.
        prediction_df["Monthly_Income"] = pd.to_numeric(
            prediction_df["Monthly_Income"],
            errors="coerce"
        )

        if pd.isna(
            prediction_df.loc[0, "Monthly_Income"]
        ):

            prediction_df.loc[
                0,
                "Monthly_Income"
            ] = get_median_income()

        # Keep the model input explicitly numeric.
        prediction_df["Monthly_Income"] = prediction_df[
            "Monthly_Income"
        ].astype(float)

    # --------------------------------------------------------
    # Encode categorical features
    # --------------------------------------------------------

    categorical_columns = [
        "Device",
        "Genre",
        "Region",
        "Payment_History",
        "Subscription_Plan"
    ]

    for column in categorical_columns:

        if column in prediction_df.columns:

            if column in label_encoders:

                encoder = label_encoders[column]

                value = prediction_df.loc[
                    0,
                    column
                ]

                # Check whether category exists
                if value not in encoder.classes_:

                    raise ValueError(
                        f"Unknown value '{value}' "
                        f"for {column}. "
                        f"Expected one of: "
                        f"{list(encoder.classes_)}"
                    )

                prediction_df[column] = (
                    encoder.transform(
                        prediction_df[column]
                    )
                )

    # --------------------------------------------------------
    # Ensure exact model feature order
    # --------------------------------------------------------

    prediction_df = prediction_df[
        features
    ]

    # --------------------------------------------------------
    # Prediction
    # --------------------------------------------------------

    prediction = model.predict(
        prediction_df
    )[0]

    probabilities = model.predict_proba(
        prediction_df
    )[0]

    churn_probability = float(
        probabilities[1]
    )

    confidence = float(
        max(probabilities) * 100
    )

    # --------------------------------------------------------
    # Risk category
    # --------------------------------------------------------

    if churn_probability < 0.30:

        risk_category = "Low Risk"

    elif churn_probability < 0.70:

        risk_category = "Medium Risk"

    else:

        risk_category = "High Risk"

    return (
        prediction,
        churn_probability,
        confidence,
        risk_category
    )


# ============================================================
# PAGE TITLE
# ============================================================

st.html(
    """
    <div class="cp-header-card">

        <div class="cp-header-title">
            🎯 Customer Churn Prediction
        </div>

        <div class="cp-header-subtitle">
            Analyze visitors, subscribers, and existing customers
            using the CustomerPulse churn prediction system.
        </div>

    </div>
    """
)


# ============================================================
# CUSTOMER TYPE
# ============================================================

customer_type = st.radio(
    "Select Customer Type",
    [
        "🆕 Visitor",
        "👤 Subscriber",
        "👑 Existing Customer"
    ],
    horizontal=True
)


# ============================================================
# VISITOR COMMON INPUTS
# ============================================================

if customer_type == "🆕 Visitor":

    st.subheader("📋 Customer Information")

    col1, col2 = st.columns(2)

    with col1:

        age = st.number_input(
            "Age",
            min_value=1,
            max_value=100,
            value=25
        )

        daily_watch_time = st.number_input(
            "Daily Watch Time (hours)",
            min_value=0.0,
            max_value=24.0,
            value=2.0,
            step=0.1
        )

        engagement_rate = st.slider(
            "Engagement Rate",
            min_value=0,
            max_value=100,
            value=50
        )

        customer_satisfaction = st.slider(
            "Customer Satisfaction",
            min_value=1,
            max_value=10,
            value=7
        )

    with col2:

        device = st.selectbox(
            "Device",
            get_category_options("Device")
        )

        genre = st.selectbox(
            "Favorite Genre",
            get_category_options("Genre")
        )

        region = st.selectbox(
            "Region",
            get_category_options("Region")
        )

        # ====================================================
        # OPTIONAL MONTHLY INCOME
        # ====================================================

        monthly_income_input = st.text_input(
            "Monthly Income (Optional)",
            placeholder="Enter income or leave blank"
        )

        if monthly_income_input.strip() == "":
            monthly_income = None

        else:

            try:

                monthly_income = float(
                    monthly_income_input
                )

                if monthly_income < 0:
                    st.error(
                        "Monthly Income cannot be negative."
                    )
                    monthly_income = None

            except ValueError:

                st.error(
                    "Please enter a valid number for Monthly Income."
                )

                monthly_income = None


# ============================================================
# VISITOR
# ============================================================

if customer_type == "🆕 Visitor":

    st.divider()

    st.subheader("🆕 Visitor Analysis")


    if st.button(
        "🔍 Analyze Visitor",
        width="stretch",
        key="analyze_visitor"
    ):

        visitor_customer = {

            "Subscription_Length": 0,

            "Customer_Satisfaction":
                customer_satisfaction,

            "Daily_Watch_Time":
                daily_watch_time,

            "Engagement_Rate":
                engagement_rate,

            "Device":
                device,

            "Genre":
                genre,

            "Region":
                region,

            "Payment_History":
                "On-Time",

            "Subscription_Plan":
                "Basic",

            "Support_Queries":
                0,

            "Age":
                int(age),

            "Monthly_Income":
                monthly_income,

            "Promotional_Offers":
                0,

            "Profiles_Created":
                1,

            "Days_Since_Last_Activity":
                0
        }

        try:

            (
                prediction,
                probability,
                confidence,
                risk_category
            ) = predict_customer(
                visitor_customer
            )

            recommendations = get_recommendations(
                visitor_customer,
                probability,
                "visitor"
            )

            st.session_state[
                "visitor_analysis"
            ] = {
                "customer": visitor_customer,
                "prediction": prediction,
                "probability": probability,
                "confidence": confidence,
                "risk": risk_category,
                "recommendations": recommendations
            }

        except Exception as e:

            st.error(
                f"Visitor analysis failed: {e}"
            )

    # --------------------------------------------------------
    # SHOW VISITOR RESULT
    # --------------------------------------------------------

    if "visitor_analysis" in st.session_state:

        result = st.session_state[
            "visitor_analysis"
        ]

        st.subheader("🎯 Visitor Analysis Result")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "Churn Probability",
                f"{result['probability'] * 100:.2f}%"
            )

        with col2:
            st.metric(
                "Risk Category",
                result["risk"]
            )

        with col3:
            st.metric(
                "Confidence",
                f"{result['confidence']:.2f}%"
            )

        st.progress(
            result["probability"]
        )

        st.subheader("💡 Recommendations")

        for recommendation in result[
            "recommendations"
        ]:

            st.write(
                f"• {recommendation}"
            )

    # --------------------------------------------------------
    # ADD VISITOR
    # --------------------------------------------------------

    st.divider()

    st.subheader("💾 Database")

    if st.button(
        "➕ Add Visitor to Database",
        width="stretch",
        key="add_visitor"
    ):

        new_customer_id = generate_customer_id()

        conn = get_connection()
        cursor = conn.cursor()

        query = """
            INSERT INTO customer_data (
                Customer_ID,
                Subscription_Length,
                Customer_Satisfaction,
                Daily_Watch_Time,
                Engagement_Rate,
                Device,
                Genre,
                Region,
                Payment_History,
                Subscription_Plan,
                Churn,
                Support_Queries,
                Age,
                Monthly_Income,
                Promotional_Offers,
                Profiles_Created,
                Days_Since_Last_Activity
            )
            VALUES (
                %s, %s, %s, %s, %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s, %s, %s, %s
            )
        """

        values = (

            new_customer_id,

            0,

            customer_satisfaction,

            daily_watch_time,

            engagement_rate,

            device,

            genre,

            region,

            "On-Time",

            "Basic",

            "No",

            0,

            age,

            monthly_income,

            0,

            1,

            0
        )

        cursor.execute(
            query,
            values
        )

        conn.commit()

        cursor.close()
        conn.close()

        st.session_state[
            "new_visitor_id"
        ] = new_customer_id

        st.success(
            f"✅ Visitor added successfully! "
            f"Customer ID: **{new_customer_id}**"
        )

        # Refresh database data immediately.
        st.rerun()

    # --------------------------------------------------------
    # DELETE VISITOR
    # --------------------------------------------------------

    if "new_visitor_id" in st.session_state:

        visitor_id = st.session_state[
            "new_visitor_id"
        ]

        st.warning(
            f"Added Visitor Customer ID: "
            f"**{visitor_id}**"
        )

        if st.button(
            "🗑️ Delete Added Visitor",
            width="stretch",
            key="delete_visitor"
        ):

            deleted = delete_customer(
                visitor_id
            )

            if deleted:

                st.success(
                    f"Customer {visitor_id} "
                    "deleted successfully."
                )

                del st.session_state[
                    "new_visitor_id"
                ]

                st.rerun()

            else:

                st.error(
                    "Customer could not be deleted."
                )


# ============================================================
# SUBSCRIBER
# ============================================================

elif customer_type == "👤 Subscriber":

    st.divider()

    # --------------------------------------------------------
    # 1. SUBSCRIBER INFORMATION
    # --------------------------------------------------------

    st.subheader("👤 Subscriber Information")

    # --------------------------------------------------------
    # Subscriber customers are loaded from the database.
    # New customers created through the Visitor section use
    # IDs greater than the original C00001-C01000 dataset.
    # This keeps the Subscriber list persistent after reruns.
    # --------------------------------------------------------

    customer_id_series = customers["Customer_ID"].astype(str)

    new_customer_numbers = pd.to_numeric(
        customer_id_series.str.replace(
            "C", "", regex=False
        ),
        errors="coerce"
    )

    subscriber_customers = customers[
        new_customer_numbers > 1000
    ].copy()

    subscriber_customers = subscriber_customers.sort_values(
        "Customer_ID"
    )

    subscriber_customer_ids = (
        subscriber_customers["Customer_ID"]
        .astype(str)
        .tolist()
    )

    if subscriber_customer_ids:

        selected_subscriber_id = st.selectbox(
            "Customer ID",
            subscriber_customer_ids,
            key="subscriber_customer_select"
        )

        selected_subscriber = subscriber_customers[
            subscriber_customers["Customer_ID"].astype(str)
            == selected_subscriber_id
        ].iloc[0]

        current_subscription_length = int(
            pd.to_numeric(
                selected_subscriber["Subscription_Length"],
                errors="coerce"
            )
            if pd.notna(
                selected_subscriber["Subscription_Length"]
            )
            else 0
        )

    else:

        selected_subscriber_id = None
        selected_subscriber = None
        current_subscription_length = 0

        st.info(
            "Add a Visitor first to create a Subscriber."
        )

    # --------------------------------------------------------
    # 2. SUBSCRIBER DETAILS
    # --------------------------------------------------------

    st.divider()

    st.subheader("💳 Subscriber Details")

    subscriber_customer = None

    if selected_subscriber is not None:

        st.info(
            f"Current Subscription Length: "
            f"**{current_subscription_length} months**"
        )

        detail_col1, detail_col2 = st.columns(2)

        with detail_col1:

            remaining_months = max(
                0,
                12 - current_subscription_length
            )

            if remaining_months > 0:

                new_subscription_length = st.number_input(
                    "Subscription Length (months)",
                    min_value=1,
                    max_value=remaining_months,
                    value=1,
                    step=1,
                    key=f"subscriber_length_{selected_subscriber_id}"
                )

            else:

                new_subscription_length = 0

                st.info(
                    "This customer has reached 12 months "
                    "of total subscription length."
                )

            subscription_plan_options = get_category_options(
                "Subscription_Plan"
            )

            current_plan = selected_subscriber[
                "Subscription_Plan"
            ]

            plan_index = (
                subscription_plan_options.index(current_plan)
                if current_plan in subscription_plan_options
                else 0
            )

            subscription_plan = st.selectbox(
                "Subscription Plan",
                subscription_plan_options,
                index=plan_index,
                key=f"subscriber_plan_{selected_subscriber_id}"
            )

        with detail_col2:

            payment_options = get_category_options(
                "Payment_History"
            )

            current_payment = selected_subscriber[
                "Payment_History"
            ]

            payment_index = (
                payment_options.index(current_payment)
                if current_payment in payment_options
                else 0
            )

            payment_history = st.selectbox(
                "Payment History",
                payment_options,
                index=payment_index,
                key=f"subscriber_payment_{selected_subscriber_id}"
            )

            promotional_offers = st.number_input(
                "Promotional Offers Used",
                min_value=0,
                max_value=20,
                value=int(
                    selected_subscriber["Promotional_Offers"]
                    if pd.notna(
                        selected_subscriber["Promotional_Offers"]
                    )
                    else 0
                ),
                key=f"subscriber_offers_{selected_subscriber_id}"
            )

            profiles_created = st.number_input(
                "Profiles Created",
                min_value=1,
                max_value=10,
                value=max(
                    1,
                    int(
                        selected_subscriber["Profiles_Created"]
                        if pd.notna(
                            selected_subscriber["Profiles_Created"]
                        )
                        else 1
                    )
                ),
                key=f"subscriber_profiles_{selected_subscriber_id}"
            )

        updated_subscription_length = (
            current_subscription_length
            + int(new_subscription_length)
        )

        st.success(
            f"After this subscription, total Subscription Length "
            f"will be: **{updated_subscription_length} months**"
        )

        subscriber_customer = selected_subscriber.to_dict()
        subscriber_customer["Subscription_Length"] = (
            updated_subscription_length
        )
        subscriber_customer["Subscription_Plan"] = subscription_plan
        subscriber_customer["Payment_History"] = payment_history
        subscriber_customer["Promotional_Offers"] = int(
            promotional_offers
        )
        subscriber_customer["Profiles_Created"] = int(
            profiles_created
        )

        if remaining_months > 0 and st.button(
            "💾 Save Subscription",
            width="stretch",
            key=f"save_subscriber_{selected_subscriber_id}"
        ):

            conn = get_connection()
            cursor = conn.cursor()

            update_query = """
                UPDATE customer_data
                SET
                    Subscription_Length = %s,
                    Payment_History = %s,
                    Subscription_Plan = %s,
                    Promotional_Offers = %s,
                    Profiles_Created = %s
                WHERE Customer_ID = %s
            """

            cursor.execute(
                update_query,
                (
                    subscriber_customer["Subscription_Length"],
                    subscriber_customer["Payment_History"],
                    subscriber_customer["Subscription_Plan"],
                    subscriber_customer["Promotional_Offers"],
                    subscriber_customer["Profiles_Created"],
                    selected_subscriber_id
                )
            )

            conn.commit()
            cursor.close()
            conn.close()

            st.success(
                f"✅ Subscription updated successfully for "
                f"Customer {selected_subscriber_id}."
            )

            st.info(
                f"Previous total: {current_subscription_length} months  |  "
                f"New subscription: {new_subscription_length} months  |  "
                f"New total: {updated_subscription_length} months"
            )

            st.rerun()

    # --------------------------------------------------------
    # 3. CUSTOMER ANALYSIS
    # --------------------------------------------------------

    st.divider()

    st.subheader("📊 Customer Analysis")

    if subscriber_customer is not None:

        if st.button(
            "🔍 Analyze Customer",
            width="stretch",
            key="analyze_subscriber_customer"
        ):

            try:

                # MySQL decimal values can arrive as Python Decimal/object
                # values. Convert the numeric model fields before prediction.
                subscriber_prediction_customer = subscriber_customer.copy()

                numeric_model_features = [
                    "Subscription_Length",
                    "Customer_Satisfaction",
                    "Daily_Watch_Time",
                    "Engagement_Rate",
                    "Support_Queries",
                    "Age",
                    "Monthly_Income",
                    "Promotional_Offers",
                    "Profiles_Created",
                    "Days_Since_Last_Activity"
                ]

                for numeric_feature in numeric_model_features:
                    if numeric_feature in subscriber_prediction_customer:
                        subscriber_prediction_customer[numeric_feature] = pd.to_numeric(
                            subscriber_prediction_customer[numeric_feature],
                            errors="coerce"
                        )

                (
                    prediction,
                    probability,
                    confidence,
                    risk_category
                ) = predict_customer(
                    subscriber_prediction_customer
                )

                recommendations = get_recommendations(
                    subscriber_prediction_customer,
                    probability,
                    "subscriber"
                )

                st.session_state[
                    "subscriber_analysis"
                ] = {
                    "customer": subscriber_prediction_customer,
                    "prediction": prediction,
                    "probability": probability,
                    "confidence": confidence,
                    "risk": risk_category,
                    "recommendations": recommendations
                }

            except Exception as e:

                st.error(
                    f"Customer analysis failed: {e}"
                )

    if "subscriber_analysis" in st.session_state:

        result = st.session_state[
            "subscriber_analysis"
        ]

        st.subheader("🎯 Analysis Result")

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric(
                "Churn Probability",
                f"{result['probability'] * 100:.2f}%"
            )

        with col2:
            st.metric(
                "Risk Category",
                result["risk"]
            )

        with col3:
            st.metric(
                "Confidence",
                f"{result['confidence']:.2f}%"
            )

        st.progress(result["probability"])

        st.subheader("💡 Recommendations")

        for recommendation in result[
            "recommendations"
        ]:
            st.write(
                f"• {recommendation}"
            )

    # --------------------------------------------------------
    # 4. DOWNLOAD SUBSCRIBER LIST
    # --------------------------------------------------------

    st.divider()

    st.subheader("📄 Subscriber List")

    if subscriber_customer_ids:

        # Reload the current Subscriber rows from the database so
        # the PDF always contains the latest saved values.
        report_customers = customers[
            customers["Customer_ID"].astype(str).isin(
                [str(x) for x in subscriber_customer_ids]
            )
        ].copy()

        from io import BytesIO
        from reportlab.lib import colors
        from reportlab.lib.enums import TA_CENTER
        from reportlab.lib.pagesizes import A4, landscape
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.platypus import (
            SimpleDocTemplate,
            Paragraph,
            Spacer,
            Table,
            TableStyle
        )

        pdf_buffer = BytesIO()

        doc = SimpleDocTemplate(
            pdf_buffer,
            pagesize=landscape(A4),
            rightMargin=25,
            leftMargin=25,
            topMargin=25,
            bottomMargin=25
        )

        styles = getSampleStyleSheet()

        title_style = ParagraphStyle(
            "CustomerPulseTitle",
            parent=styles["Title"],
            alignment=TA_CENTER,
            fontName="TimesNewRoman-Bold",
            fontSize=20,
            spaceAfter=6
        )

        subtitle_style = ParagraphStyle(
            "CustomerPulseSubtitle",
            parent=styles["Normal"],
            alignment=TA_CENTER,
            fontName="TimesNewRoman",
            fontSize=12,
            spaceAfter=15
        )

        cell_style = ParagraphStyle(
            "CustomerPulseCell",
            parent=styles["Normal"],
            fontName="TimesNewRoman",
            fontSize=7
        )

        header_style = ParagraphStyle(
            "CustomerPulseHeader",
            parent=styles["Normal"],
            fontName="TimesNewRoman-Bold",
            fontSize=7,
            leading=8
        )

        story = [
            Paragraph("CustomerPulse", title_style),
            Paragraph(
                "Subscriber List Report",
                subtitle_style
            ),
            Spacer(1, 8)
        ]

        report_columns = [
            "Customer_ID",
            "Subscription_Length",
            "Subscription_Plan",
            "Payment_History",
            "Customer_Satisfaction",
            "Daily_Watch_Time",
            "Engagement_Rate",
            "Device",
            "Genre",
            "Region",
            "Support_Queries",
            "Age",
            "Monthly_Income",
            "Promotional_Offers",
            "Profiles_Created",
            "Days_Since_Last_Activity"
        ]

        report_data = [
            [
                Paragraph(
                    str(column).replace("_", "<br/>") ,
                    header_style
                )
                for column in report_columns
            ]
        ]

        for _, row in report_customers.iterrows():

            report_data.append([
                Paragraph(
                    str(row.get(column, "")),
                    cell_style
                )
                for column in report_columns
            ])

        table = Table(
            report_data,
            repeatRows=1,
            colWidths=[
                55, 55, 55, 55, 55, 55, 55, 50,
                50, 50, 55, 35, 60, 55, 50, 60
            ]
        )

        table.setStyle(
            TableStyle([
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#E8EEFF")),
                ("GRID", (0, 0), (-1, -1), 0.4, colors.grey),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("LEFTPADDING", (0, 0), (-1, -1), 3),
                ("RIGHTPADDING", (0, 0), (-1, -1), 3),
                ("TOPPADDING", (0, 0), (-1, -1), 3),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 3)
            ])
        )

        story.append(table)

        doc.build(story)

        st.download_button(
            "📄 Download Subscriber List",
            data=pdf_buffer.getvalue(),
            file_name="CustomerPulse_Subscriber_List.pdf",
            mime="application/pdf",
            width="stretch",
            key="subscriber_list_pdf"
        )

    else:

        st.info(
            "No Subscribers are available to download yet."
        )


# ============================================================
# EXISTING CUSTOMER
# ============================================================


elif customer_type == "👑 Existing Customer":

    st.divider()

    st.subheader("👑 Existing Customer")

    if customers.empty:

        st.warning(
            "No customers are available "
            "in the database."
        )

    else:

        customer_ids = (
            customers["Customer_ID"]
            .astype(str)
            .tolist()
        )

        selected_customer_id = st.selectbox(
            "Choose Customer ID",
            customer_ids,
            key="existing_customer_select"
        )

        selected_customer = customers[
            customers["Customer_ID"].astype(str)
            == selected_customer_id
        ].iloc[0]

        # ----------------------------------------------------
        # CURRENT DATA
        # ----------------------------------------------------

        st.subheader(
            "📊 Current Customer Data"
        )

        current_data = pd.DataFrame({

            "Feature": [

                "Customer ID",
                "Subscription Length",
                "Customer Satisfaction",
                "Daily Watch Time",
                "Engagement Rate",
                "Device",
                "Genre",
                "Region",
                "Payment History",
                "Subscription Plan",
                "Support Queries",
                "Age",
                "Monthly Income",
                "Promotional Offers",
                "Profiles Created",
                "Days Since Last Activity"
            ],

            "Current Value": [

                str(
                    selected_customer[
                        "Customer_ID"
                    ]
                ),

                selected_customer[
                    "Subscription_Length"
                ],

                selected_customer[
                    "Customer_Satisfaction"
                ],

                selected_customer[
                    "Daily_Watch_Time"
                ],

                selected_customer[
                    "Engagement_Rate"
                ],

                selected_customer[
                    "Device"
                ],

                selected_customer[
                    "Genre"
                ],

                selected_customer[
                    "Region"
                ],

                selected_customer[
                    "Payment_History"
                ],

                selected_customer[
                    "Subscription_Plan"
                ],

                selected_customer[
                    "Support_Queries"
                ],

                selected_customer[
                    "Age"
                ],

                selected_customer[
                    "Monthly_Income"
                ],

                selected_customer[
                    "Promotional_Offers"
                ],

                selected_customer[
                    "Profiles_Created"
                ],

                selected_customer[
                    "Days_Since_Last_Activity"
                ]
            ]
        })

        # Convert display values to strings so Streamlit/Arrow
        # does not mix integers, floats, strings, and None values.
        current_data = current_data.astype(str)

        st.dataframe(
            current_data,
            width="stretch",
            hide_index=True
        )

        # ----------------------------------------------------
        # MODIFY DATA
        # ----------------------------------------------------

        st.divider()

        st.subheader(
            "✏️ Modify Customer Behaviour"
        )

        col1, col2, col3 = st.columns(3)

        with col1:

            updated_watch_time = st.number_input(
                "Updated Daily Watch Time",
                min_value=0.0,
                max_value=24.0,
                value=float(
                    selected_customer[
                        "Daily_Watch_Time"
                    ]
                ),
                step=0.1,
                key=f"watch_{selected_customer_id}"
            )

            genre_options = get_category_options("Genre")

            current_genre = selected_customer[
                "Genre"
            ]

            genre_index = (
                genre_options.index(current_genre)
                if current_genre in genre_options
                else 0
            )

            updated_genre = st.selectbox(
                "Updated Genre",
                genre_options,
                index=genre_index,
                key=f"genre_{selected_customer_id}"
            )

        with col2:

            updated_satisfaction = st.slider(
                "Updated Satisfaction",
                min_value=1,
                max_value=10,
                value=int(
                    selected_customer[
                        "Customer_Satisfaction"
                    ]
                ),
                key=f"satisfaction_{selected_customer_id}"
            )

            updated_engagement = st.slider(
                "Updated Engagement Rate",
                min_value=0,
                max_value=100,
                value=int(
                    selected_customer[
                        "Engagement_Rate"
                    ]
                ),
                key=f"engagement_{selected_customer_id}"
            )

        with col3:

            updated_support_queries = st.number_input(
                "Updated Support Queries",
                min_value=0,
                max_value=100,
                value=int(
                    selected_customer[
                        "Support_Queries"
                    ]
                ),
                key=f"support_{selected_customer_id}"
            )

            updated_days_since_activity = st.number_input(
                "Updated Days Since Last Activity",
                min_value=0,
                max_value=365,
                value=int(
                    selected_customer[
                        "Days_Since_Last_Activity"
                    ]
                ),
                key=f"days_{selected_customer_id}"
            )

        # ----------------------------------------------------
        # SAVE UPDATED DATA
        # ----------------------------------------------------

        if st.button(
            "💾 Save Updated Data",
            width="stretch",
            key=f"save_{selected_customer_id}"
        ):

            updated_customer_data = (
                selected_customer.to_dict()
            )

            updated_customer_data[
                "Daily_Watch_Time"
            ] = updated_watch_time

            updated_customer_data[
                "Genre"
            ] = updated_genre

            updated_customer_data[
                "Customer_Satisfaction"
            ] = updated_satisfaction

            updated_customer_data[
                "Engagement_Rate"
            ] = updated_engagement

            updated_customer_data[
                "Support_Queries"
            ] = updated_support_queries

            updated_customer_data[
                "Days_Since_Last_Activity"
            ] = updated_days_since_activity

            st.session_state[
                "updated_customer_data"
            ] = updated_customer_data

            st.session_state[
                "updated_customer_id"
            ] = selected_customer_id

            # Clear old prediction
            st.session_state.pop(
                "latest_prediction",
                None
            )

            st.session_state.pop(
                "latest_probability",
                None
            )

            st.session_state.pop(
                "latest_risk",
                None
            )

            st.session_state.pop(
                "latest_confidence",
                None
            )

            st.success(
                "✅ Customer changes saved temporarily."
            )

        # ----------------------------------------------------
        # VIEW UPDATED CUSTOMER DATA
        # ----------------------------------------------------

        has_saved_data = (
            "updated_customer_data"
            in st.session_state
            and
            st.session_state.get(
                "updated_customer_id"
            ) == selected_customer_id
        )

        if has_saved_data:

            updated_data = st.session_state[
                "updated_customer_data"
            ]

            st.divider()

            st.subheader(
                "🔎 View Updated Customer Data"
            )

            updated_display = pd.DataFrame({

                "Feature": [

                    "Customer ID",
                    "Subscription Length",
                    "Customer Satisfaction",
                    "Daily Watch Time",
                    "Engagement Rate",
                    "Device",
                    "Genre",
                    "Region",
                    "Payment History",
                    "Subscription Plan",
                    "Support Queries",
                    "Age",
                    "Monthly Income",
                    "Promotional Offers",
                    "Profiles Created",
                    "Days Since Last Activity"
                ],

                "Updated Value": [

                    str(
                        updated_data[
                            "Customer_ID"
                        ]
                    ),

                    updated_data[
                        "Subscription_Length"
                    ],

                    updated_data[
                        "Customer_Satisfaction"
                    ],

                    updated_data[
                        "Daily_Watch_Time"
                    ],

                    updated_data[
                        "Engagement_Rate"
                    ],

                    updated_data[
                        "Device"
                    ],

                    updated_data[
                        "Genre"
                    ],

                    updated_data[
                        "Region"
                    ],

                    updated_data[
                        "Payment_History"
                    ],

                    updated_data[
                        "Subscription_Plan"
                    ],

                    updated_data[
                        "Support_Queries"
                    ],

                    updated_data[
                        "Age"
                    ],

                    updated_data[
                        "Monthly_Income"
                    ],

                    updated_data[
                        "Promotional_Offers"
                    ],

                    updated_data[
                        "Profiles_Created"
                    ],

                    updated_data[
                        "Days_Since_Last_Activity"
                    ]
                ]
            })

            # Convert display values to strings to avoid
            # Arrow mixed-type conversion warnings.
            updated_display = updated_display.astype(str)

            st.dataframe(
                updated_display,
                width="stretch",
                hide_index=True
            )

            # ------------------------------------------------
            # PREDICT
            # ------------------------------------------------

            st.divider()

            if st.button(
                "🔍 Predict Churn",
                width="stretch",
                key=f"predict_{selected_customer_id}"
            ):

                try:

                    (
                        prediction,
                        probability,
                        confidence,
                        risk_category
                    ) = predict_customer(
                        updated_data
                    )

                    recommendations = (
                        get_recommendations(
                            updated_data,
                            probability
                        ,
                            "existing"
                        )
                    )

                    st.session_state[
                        "latest_prediction"
                    ] = prediction

                    st.session_state[
                        "latest_probability"
                    ] = probability

                    st.session_state[
                        "latest_risk"
                    ] = risk_category

                    st.session_state[
                        "latest_confidence"
                    ] = confidence

                    st.session_state[
                        "latest_recommendations"
                    ] = recommendations

                except Exception as e:

                    st.error(
                        f"Prediction failed: {e}"
                    )

            # ------------------------------------------------
            # PREDICTION RESULT
            # ------------------------------------------------

            if (
                "latest_prediction"
                in st.session_state
            ):

                probability = (
                    st.session_state[
                        "latest_probability"
                    ]
                )

                risk = (
                    st.session_state[
                        "latest_risk"
                    ]
                )

                confidence = (
                    st.session_state[
                        "latest_confidence"
                    ]
                )

                st.subheader(
                    "🎯 Churn Prediction Result"
                )

                col1, col2, col3 = st.columns(3)

                with col1:

                    st.metric(
                        "Churn Probability",
                        f"{probability * 100:.2f}%"
                    )

                with col2:

                    st.metric(
                        "Risk Category",
                        risk
                    )

                with col3:

                    st.metric(
                        "Confidence",
                        f"{confidence:.2f}%"
                    )

                st.progress(
                    probability
                )

                if risk == "Low Risk":

                    st.success(
                        "🟢 Customer has a low "
                        "probability of churn."
                    )

                elif risk == "Medium Risk":

                    st.warning(
                        "🟡 Customer has a moderate "
                        "probability of churn."
                    )

                else:

                    st.error(
                        "🔴 Customer has a high "
                        "probability of churn."
                    )

                # ------------------------------------------------
                # BEFORE VS AFTER
                # ------------------------------------------------

                st.subheader(
                    "📊 Before vs After"
                )

                comparison = pd.DataFrame({

                    "Feature": [

                        "Daily Watch Time",
                        "Customer Satisfaction",
                        "Engagement Rate",
                        "Genre",
                        "Support Queries",
                        "Days Since Last Activity"
                    ],

                    "Before": [

                        selected_customer[
                            "Daily_Watch_Time"
                        ],

                        selected_customer[
                            "Customer_Satisfaction"
                        ],

                        selected_customer[
                            "Engagement_Rate"
                        ],

                        selected_customer[
                            "Genre"
                        ],

                        selected_customer[
                            "Support_Queries"
                        ],

                        selected_customer[
                            "Days_Since_Last_Activity"
                        ]
                    ],

                    "After": [

                        updated_data[
                            "Daily_Watch_Time"
                        ],

                        updated_data[
                            "Customer_Satisfaction"
                        ],

                        updated_data[
                            "Engagement_Rate"
                        ],

                        updated_data[
                            "Genre"
                        ],

                        updated_data[
                            "Support_Queries"
                        ],

                        updated_data[
                            "Days_Since_Last_Activity"
                        ]
                    ]
                })

                # Convert values to strings to avoid
                # Arrow mixed-type conversion warnings.
                comparison = comparison.astype(str)

                st.dataframe(
                    comparison,
                    width="stretch",
                    hide_index=True
                )

                # ------------------------------------------------
                # RECOMMENDATIONS
                # ------------------------------------------------

                st.subheader(
                    "💡 Retention Recommendations"
                )

                recommendations = (
                    st.session_state.get(
                        "latest_recommendations",
                        []
                    )
                )

                for recommendation in recommendations:

                    st.write(
                        f"• {recommendation}"
                    )

                # ------------------------------------------------
                # DOWNLOAD CUSTOMER REPORT
                # ------------------------------------------------

                st.divider()

                from io import BytesIO
                from reportlab.lib import colors
                from reportlab.lib.enums import TA_CENTER
                from reportlab.lib.pagesizes import A4
                from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
                from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle

                pdf_buffer = BytesIO()

                doc = SimpleDocTemplate(
                    pdf_buffer,
                    pagesize=A4,
                    rightMargin=35,
                    leftMargin=35,
                    topMargin=35,
                    bottomMargin=35
                )

                styles = getSampleStyleSheet()

                title_style = ParagraphStyle(
                    "CustomerPulseReportTitle",
                    parent=styles["Title"],
                    alignment=TA_CENTER,
                    fontName="TimesNewRoman-Bold",
                    fontSize=20,
                    spaceAfter=6
                )

                subtitle_style = ParagraphStyle(
                    "CustomerPulseReportSubtitle",
                    parent=styles["Normal"],
                    alignment=TA_CENTER,
                    fontName="TimesNewRoman",
                    fontSize=12,
                    spaceAfter=18
                )

                section_style = ParagraphStyle(
                    "CustomerPulseReportSection",
                    parent=styles["Heading2"],
                    fontName="TimesNewRoman-Bold",
                    fontSize=13,
                    spaceBefore=10,
                    spaceAfter=7
                )

                body_style = ParagraphStyle(
                    "CustomerPulseReportBody",
                    parent=styles["Normal"],
                    fontName="TimesNewRoman",
                    fontSize=9,
                    leading=12
                )

                story = [
                    Paragraph("CustomerPulse", title_style),
                    Paragraph("Customer Report", subtitle_style)
                ]

                def report_table(data):
                    table = Table(
                        data,
                        colWidths=[150, 345],
                        repeatRows=0
                    )
                    table.setStyle(
                        TableStyle([
                            ("GRID", (0, 0), (-1, -1), 0.4, colors.grey),
                            ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#EDE3F8")),
                            ("FONTNAME", (0, 0), (0, -1), "TimesNewRoman-Bold"),
                            ("FONTNAME", (1, 0), (1, -1), "TimesNewRoman"),
                            ("FONTSIZE", (0, 0), (-1, -1), 9),
                            ("VALIGN", (0, 0), (-1, -1), "TOP"),
                            ("LEFTPADDING", (0, 0), (-1, -1), 7),
                            ("RIGHTPADDING", (0, 0), (-1, -1), 7),
                            ("TOPPADDING", (0, 0), (-1, -1), 6),
                            ("BOTTOMPADDING", (0, 0), (-1, -1), 6)
                        ])
                    )
                    return table

                # Customer Information
                story.append(Paragraph("Customer Information", section_style))
                story.append(report_table([
                    ["Customer ID", str(updated_data.get("Customer_ID", selected_customer_id))],
                    ["Age", str(updated_data.get("Age", ""))],
                    ["Device", str(updated_data.get("Device", ""))],
                    ["Region", str(updated_data.get("Region", ""))]
                ]))

                # Subscription Details
                story.append(Paragraph("Subscription Details", section_style))
                story.append(report_table([
                    ["Subscription Length", f"{updated_data.get('Subscription_Length', '')} months"],
                    ["Subscription Plan", str(updated_data.get("Subscription_Plan", ""))],
                    ["Payment History", str(updated_data.get("Payment_History", ""))],
                    ["Promotional Offers", str(updated_data.get("Promotional_Offers", ""))],
                    ["Profiles Created", str(updated_data.get("Profiles_Created", ""))]
                ]))

                # Customer Behaviour
                story.append(Paragraph("Customer Behaviour", section_style))
                story.append(report_table([
                    ["Customer Satisfaction", str(updated_data.get("Customer_Satisfaction", ""))],
                    ["Daily Watch Time", str(updated_data.get("Daily_Watch_Time", ""))],
                    ["Engagement Rate", str(updated_data.get("Engagement_Rate", ""))],
                    ["Genre", str(updated_data.get("Genre", ""))],
                    ["Support Queries", str(updated_data.get("Support_Queries", ""))],
                    ["Days Since Last Activity", str(updated_data.get("Days_Since_Last_Activity", ""))],
                    ["Monthly Income", str(updated_data.get("Monthly_Income", ""))]
                ]))

                # Churn Prediction
                story.append(Paragraph("Churn Prediction", section_style))

                if "latest_prediction" in st.session_state:
                    report_probability = st.session_state.get("latest_probability", 0)
                    report_risk = st.session_state.get("latest_risk", "Not Available")
                    report_confidence = st.session_state.get("latest_confidence", 0)

                    story.append(report_table([
                        ["Churn Probability", f"{report_probability * 100:.2f}%"],
                        ["Risk Category", str(report_risk)],
                        ["Confidence", f"{report_confidence:.2f}%"]
                    ]))
                else:
                    story.append(Paragraph("Prediction: Not Available", body_style))

                # Retention Recommendations
                story.append(Paragraph("Retention Recommendations", section_style))
                report_recommendations = st.session_state.get(
                    "latest_recommendations",
                    []
                )

                if report_recommendations:
                    recommendation_data = [
                        [f"• {recommendation}"]
                        for recommendation in report_recommendations
                    ]
                    recommendation_table = Table(
                        recommendation_data,
                        colWidths=[495]
                    )
                    recommendation_table.setStyle(
                        TableStyle([
                            ("FONTNAME", (0, 0), (-1, -1), "TimesNewRoman"),
                            ("FONTSIZE", (0, 0), (-1, -1), 9),
                            ("LEFTPADDING", (0, 0), (-1, -1), 7),
                            ("RIGHTPADDING", (0, 0), (-1, -1), 7),
                            ("TOPPADDING", (0, 0), (-1, -1), 4),
                            ("BOTTOMPADDING", (0, 0), (-1, -1), 4)
                        ])
                    )
                    story.append(recommendation_table)
                else:
                    story.append(Paragraph("No recommendations available.", body_style))

                # Before vs After
                story.append(Paragraph("Before vs After", section_style))
                story.append(report_table([
                    ["Feature", "Before → After"],
                    ["Daily Watch Time", f"{selected_customer.get('Daily_Watch_Time', '')} → {updated_data.get('Daily_Watch_Time', '')}"],
                    ["Customer Satisfaction", f"{selected_customer.get('Customer_Satisfaction', '')} → {updated_data.get('Customer_Satisfaction', '')}"],
                    ["Engagement Rate", f"{selected_customer.get('Engagement_Rate', '')} → {updated_data.get('Engagement_Rate', '')}"],
                    ["Genre", f"{selected_customer.get('Genre', '')} → {updated_data.get('Genre', '')}"],
                    ["Support Queries", f"{selected_customer.get('Support_Queries', '')} → {updated_data.get('Support_Queries', '')}"],
                    ["Days Since Last Activity", f"{selected_customer.get('Days_Since_Last_Activity', '')} → {updated_data.get('Days_Since_Last_Activity', '')}"]
                ]))

                story.append(Spacer(1, 18))
                story.append(Paragraph("CustomerPulse", subtitle_style))

                doc.build(story)

                st.download_button(
                    "📄 Download Customer Report",
                    data=pdf_buffer.getvalue(),
                    file_name=f"CustomerPulse_Customer_Report_{selected_customer_id}.pdf",
                    mime="application/pdf",
                    width="stretch",
                    key=f"customer_report_{selected_customer_id}"
                )

                # ------------------------------------------------
                # UPDATE DATABASE
                # ------------------------------------------------

                st.divider()

                if st.button(
                    "➕ Update Customer Database",
                    width="stretch",
                    key=f"update_database_{selected_customer_id}"
                ):

                    conn = get_connection()
                    cursor = conn.cursor()

                    update_query = """
                        UPDATE customer_data
                        SET
                            Subscription_Length = %s,
                            Customer_Satisfaction = %s,
                            Daily_Watch_Time = %s,
                            Engagement_Rate = %s,
                            Device = %s,
                            Genre = %s,
                            Region = %s,
                            Payment_History = %s,
                            Subscription_Plan = %s,
                            Support_Queries = %s,
                            Age = %s,
                            Monthly_Income = %s,
                            Promotional_Offers = %s,
                            Profiles_Created = %s,
                            Days_Since_Last_Activity = %s
                        WHERE Customer_ID = %s
                    """

                    update_values = (

                        updated_data[
                            "Subscription_Length"
                        ],

                        updated_data[
                            "Customer_Satisfaction"
                        ],

                        updated_data[
                            "Daily_Watch_Time"
                        ],

                        updated_data[
                            "Engagement_Rate"
                        ],

                        updated_data[
                            "Device"
                        ],

                        updated_data[
                            "Genre"
                        ],

                        updated_data[
                            "Region"
                        ],

                        updated_data[
                            "Payment_History"
                        ],

                        updated_data[
                            "Subscription_Plan"
                        ],

                        updated_data[
                            "Support_Queries"
                        ],

                        updated_data[
                            "Age"
                        ],

                        updated_data[
                            "Monthly_Income"
                        ],

                        updated_data[
                            "Promotional_Offers"
                        ],

                        updated_data[
                            "Profiles_Created"
                        ],

                        updated_data[
                            "Days_Since_Last_Activity"
                        ],

                        selected_customer_id
                    )

                    cursor.execute(
                        update_query,
                        update_values
                    )

                    conn.commit()

                    cursor.close()
                    conn.close()

                    st.success(
                        f"✅ Customer "
                        f"{selected_customer_id} "
                        "updated successfully in "
                        "the database."
                    )

        # ----------------------------------------------------
        # DELETE EXISTING CUSTOMER
        # ----------------------------------------------------

        st.divider()

        st.subheader(
            "🗑️ Customer Management"
        )

        st.warning(
            f"Selected Customer: "
            f"**{selected_customer_id}**"
        )

        if st.button(
            "🗑️ Delete Selected Customer",
            width="stretch",
            key=f"delete_existing_{selected_customer_id}"
        ):

            deleted = delete_customer(
                selected_customer_id
            )

            if deleted:

                st.success(
                    f"Customer "
                    f"{selected_customer_id} "
                    "deleted successfully."
                )

                # Clear session state
                for key in [
                    "updated_customer_data",
                    "updated_customer_id",
                    "latest_prediction",
                    "latest_probability",
                    "latest_risk",
                    "latest_confidence",
                    "latest_recommendations"
                ]:

                    st.session_state.pop(
                        key,
                        None
                    )

                st.rerun()

            else:

                st.error(
                    "Customer could not be deleted."
                )


# ============================================================
# FOOTER
# ============================================================

st.html(
    f"""
    <div class="cp-footer">

        <div class="cp-footer-title">
            💜 CustomerPulse
        </div>

    </div>
    """
)
