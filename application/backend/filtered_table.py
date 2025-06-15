
import logging
from sqlalchemy import text

def create_filtered_results_table(engine):
    """
    Drops the filtered_results table and its sequence if they exist, then recreates it.
    """
    try:
        with engine.begin() as conn:
            # Drop table and sequence safely
            conn.execute(text("DROP TABLE IF EXISTS filtered_results CASCADE;"))
            conn.execute(text("DROP SEQUENCE IF EXISTS filtered_results_id_seq CASCADE;"))
            logging.info("Dropped existing filtered_results table and its sequence.")

        create_table_query = """
        CREATE TABLE filtered_results (
            id SERIAL PRIMARY KEY,
            seccode VARCHAR(10),
            companyname VARCHAR(255),
            fiscalyearend DATE,
            quarter VARCHAR(10),
            growth_percentage NUMERIC,
            projected_growth_rate NUMERIC,
            growth_percentage_opvalue NUMERIC,
            projected_growth_rate_opvalue NUMERIC,
            quarterenddate DATE,
            filingdate DATE,
            earn_flag VARCHAR(50),
            div_flag VARCHAR(50),
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
        with engine.begin() as conn:
            conn.execute(text(create_table_query))
            logging.info("Created the filtered_results table successfully.")
    except Exception as e:
        logging.error(f"Error creating filtered_results table: {e}")
        raise

def insert_filtered_results(engine, filtered_data):
    """
    Inserts data into the `filtered_results` table.
    """
    insert_query = """
    INSERT INTO filtered_results (
        seccode, companyname, fiscalyearend, quarter, growth_percentage,
        projected_growth_rate, growth_percentage_opvalue, projected_growth_rate_opvalue,
        quarterenddate, filingdate, earn_flag, div_flag
    ) VALUES (
        :seccode, :companyname, :fiscalyearend, :quarter, :growth_percentage,
        :projected_growth_rate, :growth_percentage_opvalue, :projected_growth_rate_opvalue,
        :quarterenddate, :filingdate, :earn_flag, :div_flag
    );
    """
    
    logging.debug("Preparing to insert %d rows into filtered_results...", len(filtered_data))
    logging.debug("First 3 rows to be inserted:\n%s", filtered_data.head(3).to_string())

    with engine.begin() as conn:
        for idx, (_, row) in enumerate(filtered_data.iterrows(), 1):
            try:
                conn.execute(text(insert_query), {
                    'seccode': row.get('seccode'),
                    'companyname': row.get('companyname'),
                    'fiscalyearend': row.get('fiscalyearend'),
                    'quarter': row.get('quarter'),
                    'growth_percentage': row.get('growth_percentage'),
                    'projected_growth_rate': row.get('projected_growth_rate'),
                    'growth_percentage_opvalue': row.get('growth_percentage_opvalue'),
                    'projected_growth_rate_opvalue': row.get('projected_growth_rate_opvalue'),
                    'quarterenddate': row.get('quarterenddate'),
                    'filingdate': row.get('filingdate'),
                    'earn_flag': row.get('earn_flag'),
                    'div_flag': row.get('div_flag')
                })
            except Exception as e:
                logging.error(f"Error inserting row #{idx} with seccode={row.get('seccode')}: {e}")
            if idx % 500 == 0:
                logging.debug("Inserted %d records so far...", idx)
