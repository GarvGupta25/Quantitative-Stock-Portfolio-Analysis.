import re
import pandas as pd
from sqlalchemy import create_engine
from functools import reduce

# Database configuration
DB_USER = 'root'
DB_PASSWORD = '4760'
DB_HOST = 'localhost'
DB_NAME = 'stock_market_db'
DB_TABLE = 'historical_prices'
CSV_FILE = 'nifty50_stocks.csv'

try:
    # 1. Read the wide CSV
    df = pd.read_csv(CSV_FILE)
    print("[INFO] Columns in CSV:", df.columns.tolist())
    print("[INFO] First 5 rows of raw CSV:")
    print(df.head())
    print("[INFO] DataFrame info before reshaping:")
    print(df.info())

    # Normalize ticker to lowercase for matching
    df['ticker'] = df['ticker'].str.lower()

    # 2. Melt wide format into long "tall" format
    metrics = ['open', 'high', 'low', 'close', 'volume']
    long_dfs = []
    for m in metrics:
        # Identify columns for this metric
        cols = [c for c in df.columns if c.startswith(f"('{m}',_")]
        # Melt to long
        tmp = df.melt(
            id_vars=['price_date', 'ticker'],
            value_vars=cols,
            var_name='pair',
            value_name=m
        )
        # Extract ticker from the pair string and normalize case
        tmp['pair'] = tmp['pair'].str.extract(r"\('" + m + "',_'(.+)'\)")[0].str.lower()
        # Keep only rows matching the row's ticker
        tmp = tmp[tmp['pair'] == tmp['ticker']].drop(columns='pair')
        long_dfs.append(tmp)

    # Merge all metric DataFrames on price_date and ticker
    df_long = reduce(
        lambda left, right: pd.merge(left, right, on=['price_date', 'ticker']),
        long_dfs
    )
    df = df_long

    print("[INFO] After reshaping, columns:", df.columns.tolist())
    print(f"[INFO] Rows after reshaping: {len(df)}")

    # 3. Clean DataFrame
    df.dropna(inplace=True)
    print(f"[INFO] Rows after dropna: {len(df)}")
    df['price_date'] = pd.to_datetime(df['price_date']).dt.date
    df.drop_duplicates(subset=['ticker', 'price_date'], keep='first', inplace=True)
    print(f"[INFO] Rows after drop_duplicates: {len(df)}")

    if df.empty:
        print("[WARNING] No data to load—check reshaping and cleaning steps.")
    else:
        # 4. Load into SQL
        connection_str = (
            f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
        )
        engine = create_engine(connection_str)
        print(f"[INFO] Loading {len(df)} records into '{DB_TABLE}'...")
        df.to_sql(DB_TABLE, con=engine, if_exists='append', index=False)
        print("[SUCCESS] Data loaded successfully into the database!")

except Exception as e:
    print(f"[ERROR] {e}")
