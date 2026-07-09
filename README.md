# 🎯 Political Micro-Targeting & Strategy Engine

A production-grade data engineering and predictive modeling pipeline that segments voting districts into strategic target personas and simulates voter turnout using demographic data. Designed specifically for political consulting firms to optimize campaign ad allocation and field (GOTV) operations.

---

## 🏗️ Production-Grade Architecture

The system uses a highly structured directory layout to maintain clear separation of concerns, data isolation, and scalable engineering practices:

*   **`data/`** - Isolated directory containing the relational SQLite database. Securely ignored via `.gitignore` to prevent voter data leakage.
*   **`src/`** - Core business and technical logic (modular SQL database engines, data generators, and Machine Learning pipelines).
*   **`output/`** - Serialized model binaries (`.pkl`) stored separately from presentation scripts.
*   **`app.py`** - Presentation layer utilizing Streamlit and Plotly to display real-time interactive strategy playbooks for campaign directors.

---

## 📊 Technical Capabilities & Stack

*   **Data Architecture (SQL):** Engineered relational database schemas linking voter turnout histories across multiple election cycles with demographic census data.
*   **Unsupervised Machine Learning (K-Means Clustering):** Scaled and processed key political drivers (income, degree ratios, median age, renter status) to cluster districts into 4 actionable voter personas.
*   **Supervised Machine Learning (XGBoost Regressor):** Trained a production-grade regression model to predict precinct-level voter turnout percentages on the fly based on changing demographic inputs.
*   **Visual Presentation (Streamlit & Plotly):** Built an intuitive dashboard displaying calculated metrics and strategic messaging recommendations for field campaigns.

---

## 🚀 How to Run the Project Locally

Ensure you have Python installed globally, then execute the following steps in your terminal:

1. **Install Global Dependencies:**
   ```powershell
   python -m pip install pandas numpy scikit-learn xgboost streamlit plotly
   ```

2. **Seed the Relational Database:**
   ```powershell
   python -m src.generate_data
   ```

3. **Execute the ML Training Pipeline:**
   ```powershell
   python -m src.modeling
   ```

4. **Launch the Live Campaign Dashboard:**
   ```powershell
   python -m streamlit run app.py
   ```
