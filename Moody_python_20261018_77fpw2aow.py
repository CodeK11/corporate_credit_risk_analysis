import yfinance as yf
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os

def safe_get(df, row_name, year):
    """Helper to safely extract data from yfinance statements, handling missing items."""
    if row_name in df.index:
        val = df.loc[row_name, year]
        if pd.notna(val): return val
    for idx in df.index:
        if row_name.lower() in str(idx).lower():
            val = df.loc[idx, year]
            if pd.notna(val): return val
    return 0

def calculate_credit_metrics(company_name, ticker_symbol):
    ticker = yf.Ticker(ticker_symbol)
    bs, inc, info = ticker.balance_sheet, ticker.income_stmt, ticker.info
    records = []
    
    for year in bs.columns:
        try:
            total_assets = safe_get(bs, 'Total Assets', year)
            total_liabilities = safe_get(bs, 'Total Liabilities Net Minority Interest', year)
            if total_liabilities == 0: total_liabilities = safe_get(bs, 'Total Liabilities', year)
            
            current_liabilities = safe_get(bs, 'Current Liabilities', year)
            current_assets = safe_get(bs, 'Current Assets', year)
            retained_earnings = safe_get(bs, 'Retained Earnings', year)
            market_cap = info.get('marketCap', 0) 
            
            ebit = safe_get(inc, 'EBIT', year)
            interest_exp = abs(safe_get(inc, 'Interest Expense', year))
            revenue = safe_get(inc, 'Total Revenue', year)
            
            if total_assets == 0: continue

            current_ratio = current_assets / current_liabilities if current_liabilities != 0 else np.nan
            debt_to_assets = total_liabilities / total_assets
            interest_coverage = ebit / interest_exp if interest_exp != 0 else np.nan
            
            # Altman Z-Score Components
            working_capital = current_assets - current_liabilities
            A = working_capital / total_assets
            B = retained_earnings / total_assets
            C = ebit / total_assets
            D = market_cap / total_liabilities if total_liabilities != 0 else 0
            E = revenue / total_assets
            
            altman_z = (1.2 * A) + (1.4 * B) + (3.3 * C) + (0.6 * D) + (1.0 * E)
            
            if altman_z > 2.99: risk_zone = "Safe Zone"
            elif 1.81 <= altman_z <= 2.99: risk_zone = "Grey Zone"
            else: risk_zone = "Distress Zone"

            records.append({
                'Company': company_name, 'Year': year.year, 'Total Assets': total_assets,
                'Total Liabilities': total_liabilities, 'EBIT': ebit,
                'Interest Coverage Ratio': interest_coverage, 'Current Ratio': current_ratio,
                'Debt to Assets': debt_to_assets, 'Altman Z-Score': altman_z,
                'Credit Risk Zone': risk_zone
            })
        except Exception as e: continue
            
    return pd.DataFrame(records)

# Execute Pipeline
tickers = {'Ford': 'F', 'Apple': 'AAPL', 'Delta Airlines': 'DAL'}
all_data = [calculate_credit_metrics(name, symbol) for name, symbol in tickers.items()]
master_df = pd.concat(all_data, ignore_index=True).dropna(subset=['Altman Z-Score'])
master_df.sort_values(by=['Company', 'Year'], ascending=[True, False], inplace=True)

# Export
master_df.to_csv('corporate_credit_risk_data.csv', index=False)
print("✅ Data exported to corporate_credit_risk_data.csv")

# Generate Visualization
plt.figure(figsize=(12, 6))
for company in master_df['Company'].unique():
    subset = master_df[master_df['Company'] == company].sort_values('Year')
    plt.plot(subset['Year'], subset['Altman Z-Score'], marker='o', label=company)

plt.axhline(y=2.99, color='g', linestyle='--', label='Safe Zone (2.99)')
plt.axhline(y=1.81, color='r', linestyle='--', label='Distress Zone (1.81)')
plt.title('Altman Z-Score Trend (Credit Risk Migration)')
plt.xlabel('Year')
plt.ylabel('Altman Z-Score')
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig('altman_z_score_trend.png')
print("✅ Visualization saved to altman_z_score_trend.png")