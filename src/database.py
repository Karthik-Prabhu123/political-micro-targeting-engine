import sqlite3
import os
import pandas as pd

DB_DIR = "data"
DB_NAME = os.path.join(DB_DIR, "campaign_data.db")

def get_db_connection():
    """Establishes and returns a database connection to the data folder."""
    if not os.path.exists(DB_DIR):
        os.makedirs(DB_DIR)
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    """Initializes the database schema for precincts, demographics, and elections."""
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # 1. Precinct Demographics Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS demographics (
            precinct_id TEXT PRIMARY KEY,
            county TEXT,
            median_income REAL,
            college_degree_pct REAL,
            median_age REAL,
            renter_pct REAL
        )
    ''')
    
    # 2. Historical Election Results Table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS election_history (
            precinct_id TEXT,
            election_year INTEGER,
            total_registered_voters INTEGER,
            total_votes_cast INTEGER,
            dem_votes INTEGER,
            rep_votes INTEGER,
            PRIMARY KEY (precinct_id, election_year),
            FOREIGN KEY (precinct_id) REFERENCES demographics(precinct_id)
        )
    ''')
    
    conn.commit()
    conn.close()
    print("✨ SQL Database schema initialized successfully.")

def insert_dataframe(table_name, df):
    """Helper function to insert a Pandas DataFrame into a specific SQL table."""
    conn = get_db_connection()
    df.to_sql(table_name, conn, if_exists='append', index=False)
    conn.close()

if __name__ == "__main__":
    init_db()
