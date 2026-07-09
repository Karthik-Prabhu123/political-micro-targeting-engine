import sqlite3
import pickle
import os
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from xgboost import XGBRegressor
from sklearn.model_selection import train_test_split

DB_PATH = os.path.join("data", "campaign_data.db")
OUTPUT_DIR = "output"

def load_and_engineer_features():
    """Extracts data from SQL and engineers campaign metrics."""
    conn = sqlite3.connect(DB_PATH)
    
    # SQL query joining demographic traits with the most recent (2024) election performance
    query = """
        SELECT 
            d.precinct_id,
            d.county,
            d.median_income,
            d.college_degree_pct,
            d.median_age,
            d.renter_pct,
            e.total_registered_voters,
            e.total_votes_cast,
            e.dem_votes,
            e.rep_votes,
            (CAST(e.total_votes_cast AS REAL) / e.total_registered_voters) * 100 AS turnout_pct,
            (CAST(e.dem_votes AS REAL) / e.total_votes_cast) * 100 AS dem_share_pct
        FROM demographics d
        JOIN election_history e ON d.precinct_id = e.precinct_id
        WHERE e.election_year = 2024
    """
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

def run_voter_clustering(df):
    """Segments precincts into 4 key political target personas."""
    features = ['median_income', 'college_degree_pct', 'median_age', 'renter_pct', 'dem_share_pct']
    X = df[features]
    
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    
    # 4 distinct voter groups
    kmeans = KMeans(n_clusters=4, random_state=42, n_init=10)
    df['voter_cluster'] = kmeans.fit_predict(X_scaled)
    
    # Ensure output directory exists and save models for app use
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    with open(os.path.join(OUTPUT_DIR, "scaler.pkl"), "wb") as f:
        pickle.dump(scaler, f)
    with open(os.path.join(OUTPUT_DIR, "kmeans_model.pkl"), "wb") as f:
        pickle.dump(kmeans, f)
        
    print("✅ Unsupervised Clustering Complete. Models saved to output/")
    return df

def train_turnout_predictor(df):
    """Trains an XGBoost engine to predict turnout based on demographics."""
    X = df[['median_income', 'college_degree_pct', 'median_age', 'renter_pct']]
    y = df['turnout_pct']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Production-grade XGBoost Regressor
    model = XGBRegressor(n_estimators=100, learning_rate=0.05, max_depth=4, random_state=42)
    model.fit(X_train, y_train)
    
    train_score = model.score(X_train, y_train)
    test_score = model.score(X_test, y_test)
    print(f"📊 XGBoost Train R²: {train_score:.2f} | Test R²: {test_score:.2f}")
    
    with open(os.path.join(OUTPUT_DIR, "turnout_xgboost.pkl"), "wb") as f:
        pickle.dump(model, f)
        
    print("✅ XGBoost Turnout Model Complete. Model saved to output/")

def execute_pipeline():
    print("🚀 Starting Political ML Engine Pipeline...")
    df = load_and_engineer_features()
    df_clustered = run_voter_clustering(df)
    train_turnout_predictor(df_clustered)
    
    # Save the analytical dataset back into SQL for fast dashboard queries
    conn = sqlite3.connect(DB_PATH)
    df_clustered.to_sql("model_output", conn, if_exists="replace", index=False)
    conn.close()
    print("💾 Final analytical master dataset saved to SQL as 'model_output'.")

if __name__ == "__main__":
    execute_pipeline()
