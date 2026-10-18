# Corporate Credit Risk & Financial Health Analyzer

## 📊 Project Overview
This project is an automated data pipeline designed to ingest, scrub, and analyze raw financial statements to assess corporate credit risk. Built to mimic the day-to-day workflows of Credit Ratings and Analytic Data Operations, the pipeline calculates key credit health indicators and visualizes bankruptcy risk migration over time.

## 🎯 Key Features
* **Automated Data Intake & Scrubbing:** Pulls 10 years of historical Balance Sheet and Income Statement data directly from live market APIs (`yfinance`), handling missing line items and standardizing accounting formats.
* **Credit Ratio Engine:** Automatically calculates fundamental credit metrics:
  * *Liquidity:* Current Ratio
  * *Leverage:* Debt-to-Assets Ratio
  * *Coverage:* Interest Coverage Ratio (EBIT / Interest Expense)
* **Risk Modeling (Altman Z-Score):** Implements the Altman Z-Score formula to predict bankruptcy probability, classifying companies into Safe, Grey, or Distress zones.
* **Data Quality Checks:** Programmatic validation to flag missing quarters or accounting anomalies before they reach the reporting layer.

## 🛠️ Tech Stack
* **Python:** Pandas, NumPy, yfinance, Matplotlib
* **Data Visualization:** Power BI (Dashboard provided below)
* **Domain Knowledge:** Financial Statement Analysis, Credit Risk Fundamentals, Capital Markets

## 📈 Key Insights & Visualizations
The pipeline was executed on a diverse basket of equities to test risk profiling across different economic sectors:
* **Apple (Tech):** Consistently scores in the **Safe Zone** (>2.99) due to massive retained earnings and market capitalization buffering their liabilities.
* **Ford (Auto):** Flags in the **Distress Zone** (<1.81). Auto manufacturers are highly capital-intensive and carry massive structural debt, which the Z-score correctly identifies as a leverage risk.
* **Delta Airlines (Aviation):** Scores in the **Distress Zone**, reflecting the high fixed costs and fleet-financing debt inherent to the airline industry, making them highly sensitive to macroeconomic cycles.

## 🚀 How to Run
1. Install dependencies: `pip install yfinance pandas matplotlib`
2. Run the script: `python credit_risk_pipeline.py`
3. The script will generate `corporate_credit_risk_data.csv` for use in BI tools and save a trend plot.

## 💡 Future Scope
* Integrate SQL databases to store historical ratings and perform time-series forecasting.
* Add Natural Language Processing (NLP) to scrape and analyze Earnings Call transcripts for qualitative risk sentiment.
