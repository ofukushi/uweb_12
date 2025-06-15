
# create_tables.py

import psycopg2
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv(dotenv_path='/mnt/c/Users/osamu/OneDrive/onedrive_python_source/envs/.env.uweb_11')

def get_database_connection():
    """Get a psycopg2 database connection based on environment."""
    is_heroku = True  # Force Heroku DB connection for this example
    if is_heroku:
        database_url = os.getenv('HEROKU_DATABASE_URL')
        database_url = database_url.replace('postgres://', 'postgresql://')
        print("Running in Heroku environment. Connecting to Heroku database.")
    else:
        database_url = os.getenv('LOCAL_DATABASE_URL')
        database_url = database_url.replace('postgres://', 'postgresql://')
        print("Running in local environment. Connecting to local database.")
    return psycopg2.connect(database_url)

def create_table(table_name):
    conn = get_database_connection()
    cur = conn.cursor()

    try:
        cur.execute(f'DROP TABLE IF EXISTS "{table_name}";')

        if table_name == "dividend":
            create_table_query = f'''
            CREATE TABLE "{table_name}" (
                "id" SERIAL PRIMARY KEY,
                "seccode" VARCHAR(10) UNIQUE,
                "companyname" VARCHAR(255),
                "fiscalyearend" DATE,
                "dividend_yield" NUMERIC,
                "dividend_amount" NUMERIC,
                "timestamp" TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            '''
        else:
            create_table_query = f'''
            CREATE TABLE "{table_name}" (
                "id" SERIAL PRIMARY KEY,
                "seccode" VARCHAR(10) UNIQUE,
                "companyname" VARCHAR(255),
                "fiscalyearend" DATE,
                "quarter" VARCHAR(10),
                "growth_percentage" NUMERIC,
                "projected_growth_rate" NUMERIC,
                "growth_percentage_opvalue" NUMERIC,
                "projected_growth_rate_opvalue" NUMERIC,
                "quarterenddate" DATE,
                "timestamp" TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            '''
        cur.execute(create_table_query)
        print(f"Table '{table_name}' created successfully.")

    except Exception as e:
        print(f"Error creating table '{table_name}': {e}")
    finally:
        conn.commit()
        cur.close()
        conn.close()

if __name__ == "__main__":
    try:
        create_table("growth")
        create_table("recordhigh")
        create_table("filtered_results")
        create_table("value")
        create_table("dividend")
        print("All specified tables have been created successfully.")
    except Exception as e:
        print(f"Error during table creation: {e}")
