import pickle
import os
import pandas as pd

def extract_political_drivers():
    """Extracts exactly which demographic feature drives voter turnout the most."""
    model_path = os.path.join("output", "turnout_xgboost.pkl")
    
    if not os.path.exists(model_path):
        print("❌ Run your modeling script first to generate the model!")
        return

    with open(model_path, "rb") as f:
        model = pickle.load(f)
        
    # Feature names used during training
    features = ['median_income', 'college_degree_pct', 'median_age', 'renter_pct']
    importances = model.feature_importances_
    
    print("\n🔥 --- STRATEGIC FIELD INSIGHTS (FEATURE IMPORTANCE) ---")
    for feat, imp in zip(features, importances):
        print(f"• {feat.upper().replace('_', ' ')}: {imp*100:.1f}% impact on turnout prediction.")

if __name__ == "__main__":
    extract_political_drivers()
