from mftool import Mftool
import pandas as pd
import numpy as np  
from datetime import datetime, timedelta

mf = Mftool()
all_schemes = mf.get_scheme_codes()

# --- NEW FUNCTION: THE DATA ENGINE ---
# This function does the heavy lifting to find Returns and Risk
def get_advanced_info(code):
    try:
        # 1. Get Basic Details (Manager, Type, etc.)
        details = mf.get_scheme_details(code)
        
        # 2. Get Historical Data (Last 5 Years)
        # This is where we get the data to calculate returns
        df = mf.get_scheme_historical_nav(code, as_Dataframe=True).reset_index()
        
        # Clean the data (Turn dates into real Time objects, and NAV into Numbers)
        df['date'] = pd.to_datetime(df['date'], dayfirst=True)
        df['nav'] = pd.to_numeric(df['nav'], errors='coerce')
        df = df.sort_values('date', ascending=True) # Sort Oldest to Newest

        # 3. HELPER: Calculate Returns for a specific year count
        def calculate_return(years):
            try:
                # Find date 'years' ago
                target_date = df['date'].iloc[-1] - timedelta(days=years*365)
                # Find the row closest to that date
                idx = df['date'].searchsorted(target_date)
                
                # If history is too short, return "N/A"
                if idx >= len(df): return "N/A (New Fund)"
                
                start_nav = df['nav'].iloc[idx]
                current_nav = df['nav'].iloc[-1]
                
                # Math: CAGR Formula
                cagr = ((current_nav / start_nav) ** (1/years)) - 1
                return round(cagr * 100, 2) # Return percentage
            except:
                return "N/A"

        # 4. CALCULATE RISK (Volatility)
        # Standard Deviation of daily returns is the industry standard for risk
        daily_returns = df['nav'].pct_change()
        # STEP 2: Clean the data (Remove Infinity and N/A)
        daily_returns = daily_returns.replace([np.inf, -np.inf], np.nan).dropna()
        risk = daily_returns.std() * np.sqrt(252) * 100 # Annualized Risk

        # 5. PACK EVERYTHING INTO A DICTIONARY
        info = {
            "Scheme Name": details['scheme_name'],
            "Fund House": details['fund_house'],
            "Category": details['scheme_category'],
            "Type": details['scheme_type'],
            "Current NAV": f"₹ {df['nav'].iloc[-1]}",
            "1-Year Return": f"{calculate_return(1)} %",
            "3-Year Return": f"{calculate_return(3)} %",
            "5-Year Return": f"{calculate_return(5)} %",
            "Risk (Volatility)": f"{round(risk, 2)} % (Higher is riskier)",
            "Last Updated": df['date'].iloc[-1].strftime('%d-%b-%Y')
        }
        return info

    except Exception as e:
        return None

# --- MAIN PROGRAM LOOP ---
while True:
    print("\n" + "="*50)
    print("      ADVANCED MUTUAL FUND ANALYZER      ")
    print("="*50)
    print("1. Search & Analyze Fund")
    print("2. Compare Two Funds")
    print("3. Exit")
    
    choice = input("\nEnter choice (1-3): ")

    if choice == '1':
        query = input("Enter Fund Name (e.g. Quant Small): ")
        
        # Search Logic
        matches = {k:v for k,v in all_schemes.items() if query.lower() in v.lower()}
        
        if matches:
            print(f"\nFound {len(matches)} funds. Showing top 5:")
            for c, n in list(matches.items())[:5]:
                print(f"[{c}] {n}")
            
            code = input("\nEnter Code to Analyze: ")
            if code in all_schemes:
                print("\nProcessing... fetching 5 years of data...")
                data = get_advanced_info(code)

                if data:
                    print("\n" + "-"*30)
                    print("       FUND REPORT CARD       ")
                    print("-" * 30)
                    for k, v in data.items():
                        print(f"{k:20} : {v}")
                        

                else:
                    print("Error: Could not fetch detailed history.")
            else:
                print("Invalid Code.")
        else:
            print("No funds found.")

    elif choice == '2':
        # Simple Comparison Logic using the same engine
        c1 = input("Enter First Fund Code: ")
        c2 = input("Enter Second Fund Code: ")
        
        print("\nComparing... This may take a few seconds...")
        d1 = get_advanced_info(c1)
        d2 = get_advanced_info(c2)
        
        if d1 and d2:
            # Create a comparison table using Pandas
            compare_df = pd.DataFrame([d1, d2])
            # Transpose (flip) the table so it looks like a Versus card
            print(compare_df.set_index("Scheme Name").T)
        else:
            print("One of the codes was invalid or has no data.")

    elif choice == '3':
        break