import mysql.connector
import streamlit as st
import os

# Load environment variables (for local development)
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    # dotenv not available (e.g., in Streamlit Cloud)
    pass

# Database configuration - Try to get from Streamlit secrets first, then environment
try:
    DB_CONFIG = {
        "host": st.secrets["DB_HOST"],
        "user": st.secrets["DB_USER"],
        "password": st.secrets["DB_PASSWORD"],
        "database": st.secrets["DB_NAME"]
    }
except:
    # Fallback to environment variables for local development
    DB_CONFIG = {
        "host": os.getenv("DB_HOST", "localhost"),
        "user": os.getenv("DB_USER", "root"),
        "password": os.getenv("DB_PASSWORD", "p@ssword05D"),
        "database": os.getenv("DB_NAME", "ecommerce_db")
    }

def run_sql_query(query):
    """
    Executes a SQL query on the ecommerce_db and returns the result.
    
    Args:
        query (str): The SQL query to be executed.
    
    Returns:
        list: Fetched results from the database as a list of tuples.
    """
    conn = None
    cursor = None
    try:
        conn = mysql.connector.connect(**DB_CONFIG)
        cursor = conn.cursor()
        cursor.execute(query)
        results = cursor.fetchall()
        return results
    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        # For demo purposes, return mock data if database connection fails
        return get_mock_data(query)
    except Exception as e:
        print(f"Connection error: {e}")
        st.error("Unable to connect to database. Using mock data for demonstration.")
        return get_mock_data(query)
    finally:
        if cursor is not None:
            cursor.close()
        if conn is not None:
            conn.close()

def get_mock_data(query):
    """
    Returns mock data for demonstration purposes when database is not available.
    """
    query_lower = query.lower()
    
    if "client" in query_lower and "102" in query:
        return [("John", "Doe")]
    elif "employee" in query_lower and "branch" in query_lower:
        return [("Mumbai", 5), ("Delhi", 3), ("Bangalore", 4)]
    elif "salary" in query_lower or "paid" in query_lower:
        return [("Alice Johnson", 75000), ("Bob Smith", 72000), ("Carol Davis", 68000)]
    elif "branch" in query_lower and "name" in query_lower:
        return [("Mumbai",), ("Delhi",), ("Bangalore",), ("Chennai",)]
    elif "employee" in query_lower and ("branch 1" in query_lower or "branch_id = 1" in query_lower):
        return [("Alice", "Johnson", "Manager"), ("Bob", "Smith", "Sales")]
    else:
        return [("Sample", "Data"), ("For", "Demo")]
