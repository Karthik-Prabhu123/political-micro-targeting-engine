import numpy as np
import pandas as pd
from src.database import init_db, insert_dataframe

def generate_campaign_dataset():
    init_db()
    np.random.seed(42)
    num_precincts = 200
    
    # 1. Generate Demographic Data
    precinct_ids = [f"PRC_{i:03d}" for i in range(1, num_precincts + 1)]
    counties = np.random.choice(["Westside", "Metro-Core", "East-Valley", "North-Ridge"], size=num_precincts)
    median_income = np.random.normal(65000, 18000, num_precincts).clip(30000, 140000)
    college_degree_pct = (median_income / 140000 * 60 + np.random.normal(15, 8, num_precincts)).clip(10, 95)
    median_age = np.random.normal(41, 7, num_precincts).clip(22, 68)
    renter_pct = (100 - college_degree_pct + np.random.normal(10, 10, num_precincts)).clip(5, 85)
    
    df_demo = pd.DataFrame({
        'precinct_id': precinct_ids, 'county': counties, 'median_income': median_income,
        'college_degree_pct': college_degree_pct, 'median_age': median_age, 'renter_pct': renter_pct
    })
    insert_dataframe('demographics', df_demo)
    
    # 2. Generate Historical Election Data (Years 2020, 2022, 2024)
    years = [2020, 2022, 2024]
    election_rows = []
    
    for idx, pid in enumerate(precinct_ids):
        reg_voters = int(np.random.normal(2500, 400))
        
        for yr in years:
            base_turnout_pct = 0.72 if yr != 2022 else 0.52
            turnout_modifier = (college_degree_pct[idx] / 100) * 0.15 + (median_income[idx] / 140000) * 0.05
            turnout_pct = (base_turnout_pct + turnout_modifier + np.random.normal(0, 0.03)).clip(0.3, 0.92)
            votes_cast = int(reg_voters * turnout_pct)
            
            dem_lean = 0.45 + (renter_pct[idx]/100)*0.2 - (median_age[idx]/70)*0.15 + np.random.normal(0, 0.05)
            dem_lean = np.clip(dem_lean, 0.15, 0.85)
            
            dem_votes = int(votes_cast * dem_lean)
            rep_votes = votes_cast - dem_votes
            
            election_rows.append({
                'precinct_id': pid, 'election_year': yr, 'total_registered_voters': reg_voters,
                'total_votes_cast': votes_cast, 'dem_votes': dem_votes, 'rep_votes': rep_votes
            })
            
    df_elections = pd.DataFrame(election_rows)
    insert_dataframe('election_history', df_elections)
    print(f"📊 Successfully generated and seeded database for {num_precincts} voting precincts.")

if __name__ == "__main__":
    generate_campaign_dataset()
