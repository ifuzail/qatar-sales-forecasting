import sys
import os
import pandas as pd

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from db.db_config import get_engine

def transform_and_load_sales():
    try:
        #step1: connect using sqlalchemy
        engine = get_engine()
        conn = engine.connect()

        #step2: Read staging data into DataFrame
        df = pd.read_sql("SELECT * FROM staging.stg_sales;", conn)

        if df.empty:
            print("[!] No data in staging table.")
            return
        
        #step 3: Clean and transform
        df = df.dropna(subset=["product_name", "date_sold", "quantity", "price"])

        df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce")
        df["price"] = pd.to_numeric(df["price"], errors="coerce")
        df["discount"] = pd.to_numeric(df["discount"].fillna(0), errors="coerce")

        df = df.dropna(subset=["quantity", "price", "discount"])

        df["total_sale"] = df["quantity"] * df["price"] * (1 - df["discount"] / 100)
        df["product_name"] = df["product_name"].str.strip()
        df["category"] = df["category"].str.strip()

        #step 4: Load into final sales table
        df.to_sql("stg_sales_cleaned" , engine , schema='staging' , index=False , if_exists="append", method="multi")

        print(f"[✓] Loaded {len(df)} records into final 'sales' table.")
    except Exception as e:
        print(f"[ERROR] ETL failed: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    transform_and_load_sales()