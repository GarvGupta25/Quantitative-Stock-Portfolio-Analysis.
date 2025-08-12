import pandas as pd
import numpy as np
from sqlalchemy import create_engine
import matplotlib.pyplot as plt


db_user = 'root'
db_password = '4760'  
db_host = 'localhost'
db_name = 'stock_market_db'

connection_string = f'mysql+mysqlconnector://{db_user}:{db_password}@{db_host}/{db_name}'
engine = create_engine(connection_string)

try:
    ticker_to_analyze = input("Enter the stock ticker to analyze (e.g., RELIANCE.NS): ").upper().strip()
    sql_query = f"SELECT * FROM historical_prices WHERE ticker = '{ticker_to_analyze}' ORDER BY price_date ASC"
    
    print(f"Reading data for {ticker_to_analyze} from the database...")
    df = pd.read_sql(sql_query, engine, parse_dates=['price_date'])
    df.set_index('price_date', inplace=True)

    if df.empty:
        print(f"No data found for {ticker_to_analyze}.")
    else:
       
        print("Running Monte Carlo simulation...")
        
        
        log_returns = np.log(1 + df['close'].pct_change())
        log_returns.dropna(inplace=True)
        if not log_returns.empty:
            print("\n--- Calculating Model Inputs ---")
            u = log_returns.mean()
            var = log_returns.var()
            stdev = log_returns.std()
            drift= u-(0.5*var)
            print(f"drift component {drift}")
            print (f"volatility component {stdev}")
            print("\n--- Running Monte Carlo Simulation ---")
            num_simulation = int(input("Enter the number of simulations to run (e.g., 1000): "))
            num_days=int(input("Enter the number of days to forecast (e.g., 252 for 1 year): "))
            last_price = df['close'].iloc[-1]
            simulation_df=pd.DataFrame()
            for x in range (num_simulation):
                price_series=[]
                price=last_price 
                for y in range (num_days):
                    price = price*np.exp(drift+stdev*np.random.normal(0,1))
                    price_series.append(price)
                simulation_df[f'simulation_{x+1}']=price_series
            print(f"Generated {num_simulation} simulations. Here is a sample of the results:")
            print(simulation_df.head())
            print("Simulation complete. Generating plot...")
            fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(12, 10), gridspec_kw={'height_ratios': [3, 1]})
            mean_simulation_path = simulation_df.mean(axis=1)
            final_mean_price = mean_simulation_path.iloc[-1]
            ax1.plot(simulation_df, alpha=0.1)
            ax1.plot(mean_simulation_path, color='black', linewidth=2, label='Mean Simulation Path')
            ax1.text(num_days, final_mean_price, f' {final_mean_price:.2f}', va='center')
            ax1.set_title(f'Monte Carlo Simulation: {ticker_to_analyze}')
            ax1.set_xlabel(f'{num_days} Trading Days from Today')
            ax1.set_ylabel('Predicted Stock Price')
            ax1.axhline(y=last_price, color='r', linestyle='--', label=f'Starting Price: {last_price:.2f}')
            ax1.legend()
            final_prices = simulation_df.iloc[-1]
            ax2.hist(final_prices, bins=100, color='skyblue', edgecolor='black')
            ax2.axvline(final_mean_price, color='black', linestyle='--', label=f'Mean Final Price: {final_mean_price:.2f}')
            
            ax2.set_xlabel('Final Price')
            ax2.set_ylabel('Frequency')
            ax2.legend()
            plt.tight_layout() 
            plt.show()
except Exception as e:
    print("⚠️ An error occurred during the Monte Carlo simulation:")
                