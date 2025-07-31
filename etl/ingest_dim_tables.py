import sys
import os
import pandas as pd

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from db.db_config import get_engine


def load_dim_product(df, engine):
    dim_product = df[['product_name', 'category']].drop_duplicates()
    existing = pd.read_sql("SELECT product_name, category FROM core.dim_product", engine)

    # Merge on both columns to find new rows
    merged = dim_product.merge(existing, on=['product_name', 'category'], how='left', indicator=True)
    new_rows = merged[merged['_merge'] == 'left_only'].drop(columns=['_merge'])

    if not new_rows.empty:
        new_rows.to_sql('dim_product', engine, schema='core', index=False, if_exists='append', method='multi')


def load_dim_store(df, engine):
    dim_store = df[['store_name']].drop_duplicates()

    # Add default city column
    dim_store['city'] = 'Qatar'

    # Get existing store names from DB
    existing = pd.read_sql("SELECT store_name FROM core.dim_store", engine)

    # Filter out stores already in the database
    dim_store = dim_store[~dim_store['store_name'].isin(existing['store_name'])]

    if not dim_store.empty:
        dim_store.to_sql('dim_store', engine, schema='core', index=False, if_exists="append", method='multi')


def load_dim_date(df, engine):
    df['date_sold'] = pd.to_datetime(df['date_sold'])
    dim_date = df[['date_sold']].drop_duplicates()
    dim_date['day'] = dim_date['date_sold'].dt.day
    dim_date['month'] = dim_date['date_sold'].dt.month
    dim_date['year'] = dim_date['date_sold'].dt.year
    dim_date['quarter'] = dim_date['date_sold'].dt.quarter
    dim_date['weekday'] = dim_date['date_sold'].dt.day_name()
    dim_date = dim_date.rename(columns={'date_sold': 'date'})

    # Filter out existing dates
    existing = pd.read_sql("SELECT date FROM core.dim_date", engine)
    dim_date = dim_date[~dim_date['date'].isin(existing['date'])]

    if not dim_date.empty:
        dim_date.to_sql('dim_date', engine, schema='core', index=False, if_exists='append', method='multi')


def ingest_dimensions():
    engine = get_engine()
    conn = engine.connect()
    try:
        df = pd.read_sql("SELECT * FROM staging.stg_sales_cleaned", conn)

        if df.empty:
            print("[!] No data found in staging.stg_sales_cleaned.")
            return

        load_dim_product(df, engine)
        load_dim_store(df, engine)
        load_dim_date(df, engine)

        print("[✓] Dimension tables successfully populated.")
    except Exception as e:
        print(f"[ERROR] Failed to populate dimension tables: {e}")
    finally:
        conn.close()


if __name__ == "__main__":
    ingest_dimensions()
