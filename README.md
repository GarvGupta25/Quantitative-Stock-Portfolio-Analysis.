# Quantitative-Stock-Portfolio-Analysis.
This project is an end-to-end financial analysis tool built in Python. It engineers a data pipeline to collect historical price data for Nifty 50 stocks, stores it in a MySQL database, and uses a Monte Carlo simulation to forecast the future value of user-defined, multi-asset stock portfolios
Tech Stack
Language: Python
Data Analysis & Modeling: Pandas, NumPy
Data Collection: yfinance API
Database: MySQL
Visualization: Matplotlib
Key Features
Automated Data Pipeline: The master_run.py script automatically resets the database table, downloads the latest 5 years of historical data for a list of stocks, cleans it, and loads it into a MySQL database.
Interactive Portfolio Definition: The analysis.py script prompts the user to build a portfolio by entering multiple stock tickers and their corresponding share counts.
Quantitative Forecasting: Implements a Monte Carlo simulation to project the portfolio's future value over thousands of potential outcomes.
Statistical Analysis: Calculates the combined drift and volatility of the entire portfolio to generate a statistically-backed forecast.
Rich Visualization: Generates a comprehensive chart showing:
A "cloud" of all 1,000+ simulation paths.
the mean (average) expected path of the portfolio's value.
A text annotation displaying the final predicted mean value.
A histogram showing the probability distribution of all final-day outcome
