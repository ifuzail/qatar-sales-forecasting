# db/staging/load_stg_sales_data.py

import pandas as pd
import os
import sys
from sqlalchemy import text

# Get base and data paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA_DIR = os.path.join(BASE_DIR, 'data', 'raw', 'supermarkets-datasets')

sys.path.insert(0, BASE_DIR)
from db.db_config import get_engine

# Define all store configurations
stores = [
    {
        'filename': 'lulu_al_gharaffa_qatar_sales_data.csv',
        'store_id': 1,
        'store_name': 'Lulu Hypermarket Al Gharrafa',
        'region': 'Qatar'
    },
    {
        'filename': 'lulu_al_khor_qatar_sales_data.csv',
        'store_id': 2,
        'store_name': 'Lulu Hypermarket Al Khor',
        'region': 'Qatar'
    },
    {
        'filename': 'lulu_al_wakrah_qatar_sales_data.csv',
        'store_id': 3,
        'store_name': 'Lulu Hypermarket Al Wakrah',
        'region': 'Qatar'
    },
]

def load_sales_data():
    combined_df = pd.DataFrame()

    for store in stores:
        file_path = os.path.join(DATA_DIR, store['filename'])
        try:
            df = pd.read_csv(file_path)
            df['store_id'] = store['store_id']
            df['store_name'] = store['store_name']
            df['region'] = store['region']


            combined_df = pd.concat([combined_df, df], ignore_index=True)
            print(f"✅ Loaded {store['filename']}")
        except FileNotFoundError:
            print(f"❌ File not found: {file_path}")
        except Exception as e:
            print(f"❌ Error loading {store['filename']}: {e}")
    if not combined_df.empty:
        try: 
           engine = get_engine()
           with engine.begin() as conn:
               combined_df.to_sql("stg_sales", con=conn,  schema="staging", if_exists='replace', index=False)
           print("✅ All sales data loaded into staging.stg_sales_data")  
        except Exception as e:
            print(f"❌ Failed to write to database: {e}")
    else:
        print("⚠️ No data to load into the database.")

if __name__ == "__main__":
    load_sales_data()