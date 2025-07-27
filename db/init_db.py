"""
Script Purpose:
This script initializes the PostgreSQL database environment for the Lulu Sales Forecasting project.

It performs the following actions:
1. Loads database configuration from a `.env` file.
2. Connects to the default 'postgres' database using admin credentials.
3. Checks if the target project database exists; if so, drops it.
4. Recreates the target project database.
5. Connects to the newly created database.
6. Creates the required schemas: 
   - 'staging' for raw data ingestion,
   - 'core' for cleaned and transformed data.

Use this script at the start of your workflow to ensure a fresh and consistent database environment.
"""

import os
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL
import psycopg2


# Load environment variables
load_dotenv()

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")
ADMIN_DB = os.getenv("ADMIN_DB")

admin_conn = psycopg2.connect(
    dbname=ADMIN_DB,
    user=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST,
    port=DB_PORT
)
admin_conn.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
admin_cur = admin_conn.cursor()

# Kill active connections to the target DB

admin_cur.execute(f"""
    SELECT pg_terminate_backend(pid)
    FROM pg_stat_activity
    WHERE datname = '{DB_NAME}';
""")

admin_cur.execute(f'DROP DATABASE IF EXISTS {DB_NAME};')
admin_cur.execute(f"CREATE DATABASE {DB_NAME};")

admin_cur.close()
admin_conn.close()

#Connect using SQLAlchemy

url = URL.create(
    drivername="postgresql+psycopg2",
    username=DB_USER,
    password=DB_PASSWORD,
    host=DB_HOST,
    port=DB_PORT,
    database=DB_NAME,
)
engine = create_engine(url)

# Create Schemas
with engine.connect() as conn:
    conn.execute(text("CREATE SCHEMA IF NOT EXISTS staging;"))
    conn.execute(text("CREATE SCHEMA IF NOT EXISTS core;"))
    conn.commit()


print(f" -------- Database '{DB_NAME}' recreated and schemas 'staging' and 'core' initialized. ---------")
