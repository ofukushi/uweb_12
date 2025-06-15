
# 📄file: reset_ids_all_tables.py

from sqlalchemy import create_engine, text
import logging
import os

logging.basicConfig(level=logging.INFO)

def reset_ids_all_tables(engine):
    tables = ['growth', 'dividend', 'recordhigh', 'value']
    try:
        with engine.begin() as conn:
            for table in tables:
                logging.info(f"Resetting sequential IDs for table: {table}")
                conn.execute(text(f"SELECT reset_sequential_ids('{table}')"))
        logging.info("✅ Successfully reset IDs for all tables.")
    except Exception as e:
        logging.error(f"❌ Failed to reset IDs: {e}")

if __name__ == "__main__":
    db_url = os.getenv("DATABASE_URL")
    if not db_url:
        raise EnvironmentError("DATABASE_URL environment variable not set")
    
    engine = create_engine(db_url)
    reset_ids_all_tables(engine)


# # Navigate to:
# # bash
# cd sql

# # 🔧 Step 1: Set environment variable (optional for Python use)
# export DATABASE_URL="postgresql+psycopg2://u4gfsf6lr4e5sj:p37e834285e1c5161de955adf23c5304df5878d00cb78847100ffac916c995840@ceqbglof0h8enj.cluster-czrs8kj4isg7.us-east-1.rds.amazonaws.com:5432/d1kmc11fnhb6np"

# # 🔧 Step 2: Load the SQL function into your DB
# psql "host=ceqbglof0h8enj.cluster-czrs8kj4isg7.us-east-1.rds.amazonaws.com port=5432 dbname=d1kmc11fnhb6np user=u4gfsf6lr4e5sj password=p37e834285e1c5161de955adf23c5304df5878d00cb78847100ffac916c995840" -f sql/fix_ids_function.sql

# # 🔧 Step 3: Run your Python script
# python reset_ids_all_tables.py

