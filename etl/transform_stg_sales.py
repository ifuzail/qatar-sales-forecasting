import sys
import os
import pandas as pd
from sqlalchemy import text  

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from db.db_config import get_engine

def transform_and_load_sales():
    try:
        engine = get_engine()

        with engine.connect() as conn:
            df = pd.read_sql("SELECT * FROM staging.stg_sales;", conn)

        if df.empty:
            print("[!] No data in staging table.")
            return

        # Clean and transform
        df = df.dropna(subset=["product_name", "date_sold", "quantity", "price"])

        df["quantity"] = pd.to_numeric(df["quantity"], errors="coerce")
        df["price"] = pd.to_numeric(df["price"], errors="coerce")
        df["discount"] = pd.to_numeric(df["discount"].fillna(0), errors="coerce")

        df = df.dropna(subset=["quantity", "price", "discount"])

        df["total_sale"] = df["quantity"] * df["price"] * (1 - df["discount"] / 100)
        df["product_name"] = df["product_name"].str.strip()
        df["category"] = df["category"].str.strip()

        # ✅ Drop duplicates based on important columns
        df = df.drop_duplicates(subset=["product_name", "date_sold", "quantity", "price"])

        # ✅ Wrap SQL with text()
        with engine.begin() as conn:
            conn.execute(text("DELETE FROM staging.stg_sales_cleaned;"))

        df.to_sql("stg_sales_cleaned", engine, schema='staging', index=False, if_exists="append", method="multi")

        print(f"[✓] Loaded {len(df)} records into 'staging.stg_sales_cleaned'.")

    except Exception as e:
        print(f"[ERROR] ETL failed: {e}")

if __name__ == "__main__":
    transform_and_load_sales()
