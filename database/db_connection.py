import mysql.connector
import pandas as pd
import streamlit as st


def get_connection():
    """
    Create and return MySQL database connection.
    """

    try:
            
        connection = mysql.connector.connect(
            host=st.secrets["mysql"]["host"],
            port=st.secrets["mysql"]["port"],
            user=st.secrets["mysql"]["user"],
            password=st.secrets["mysql"]["password"],
            database=st.secrets["mysql"]["database"],
            ssl_ca=st.secrets["mysql"]["ssl_ca"],
            ssl_verify_cert=True,
            ssl_verify_identity=True
        )
        
        return connection

    except mysql.connector.Error as err:
        st.error(f"Database Connection Error: {err}")
        return None


def run_query(query):
    """
    Execute SQL query and return dataframe.
    """

    conn = get_connection()

    if conn is None:
        return pd.DataFrame()

    df = pd.read_sql(query, conn)

    conn.close()

    return df


def get_unique_values(column_name):
    """
    Returns unique values from a specified column.
    """
    query = f"""
        SELECT DISTINCT {column_name}
        FROM netflix_churn
        ORDER BY {column_name}
    """

    df = run_query(query)

    return df[column_name].tolist()