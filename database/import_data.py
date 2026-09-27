import pandas as pd
import mysql.connector
import streamlit as st
# Read CSV
data = pd.read_csv(r"D:\Customer A & R\data\processed\cleaned.csv")

# Connect to MySQL
conn = mysql.connector.connect(
    host=st.secrets["mysql"]["host"],
    user=st.secrets["mysql"]["user"],
    password=st.secrets["mysql"]["password"],
    database=st.secrets["mysql"]["database"]
)

cursor = conn.cursor()
cursor.execute("TRUNCATE TABLE netflix_churn")

query = """
INSERT INTO netflix_churn
(Customer_ID, Subscription_Length, Customer_Satisfaction,
Daily_Watch_Time, Engagement_Rate, Device, Genre,
Region, Payment_History, Subscription_Plan,
Churn, Support_Queries, Age, Monthly_Income,
Promotional_Offers, Profiles_Created,
Days_Since_Last_Activity)
VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
"""

data = data.where(pd.notnull(data), None)

cursor.executemany(query, data.values.tolist())

conn.commit()

print(f"{cursor.rowcount} rows inserted successfully!")

cursor.close()
conn.close()