import mysql.connector 

# Database configuration
DB_CONFIG = {
    "host": "localhost",
    "user": "root",
    "password": "p@ssword05D",
    "database": "ecommerce_db"
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
        raise
    finally:
        if cursor is not None:
            cursor.close()
        if conn is not None:
            conn.close()
