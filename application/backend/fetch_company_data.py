

import logging
import pandas as pd
from sqlalchemy import text

def fetch_filtered_companies(engine, growth_percentage_threshold, projected_growth_rate_threshold, 
                             growth_percentage_opvalue_threshold, projected_growth_rate_opvalue_threshold, 
                             start_date, data_years, filingdate):
    logging.info("Executing query on the following database: %s", engine.url)
    logging.info("Parameters used: start_date=%s, data_years=%s, filingdate=%s", start_date, data_years, filingdate)

    years_filter_condition = f"""
    HAVING EXTRACT(YEAR FROM MAX("quarterenddate"::DATE)) - EXTRACT(YEAR FROM MIN("quarterenddate"::DATE)) + 1 >= {data_years}
    """ if data_years is not None else ""

    base_condition_parts = []
    if isinstance(growth_percentage_threshold, (int, float)):
        base_condition_parts.append(f'n."growth_percentage" >= {growth_percentage_threshold} AND n."growth_percentage" IS NOT NULL')
    if isinstance(projected_growth_rate_threshold, (int, float)):
        base_condition_parts.append(f'n."projected_growth_rate" >= {projected_growth_rate_threshold} AND n."projected_growth_rate" IS NOT NULL')
    if isinstance(growth_percentage_opvalue_threshold, (int, float)):
        base_condition_parts.append(f'b."growth_percentage_opvalue" >= {growth_percentage_opvalue_threshold} AND b."growth_percentage_opvalue" IS NOT NULL')
    if isinstance(projected_growth_rate_opvalue_threshold, (int, float)):
        base_condition_parts.append(f'b."projected_growth_rate_opvalue" >= {projected_growth_rate_opvalue_threshold} AND b."projected_growth_rate_opvalue" IS NOT NULL')
    if filingdate:
        base_condition_parts.append(f"n.\"filingdate\" = '{filingdate}'::date")

    base_condition = " AND ".join(base_condition_parts)

    where_conditions = 'n."companyname" != \'Unknown\''
    if base_condition:
        where_conditions += f" AND {base_condition}"

    start_date_condition = f"""AND "quarterenddate"::date >= '{start_date}'::date""" if start_date else ""

    query = f"""
        WITH filtered_seccode AS (
            SELECT 
                "seccode",
                EXTRACT(YEAR FROM MAX("quarterenddate"::DATE)) - EXTRACT(YEAR FROM MIN("quarterenddate"::DATE)) + 1 AS years_diff
            FROM
                "d_fins_all_netsales"
            WHERE
                "companyname" != 'Unknown'
            GROUP BY "seccode"
            {years_filter_condition}
        ),
        latest_records AS (
            SELECT 
                n."seccode",
                n."companyname",
                n."fiscalyearend",
                n."growth_percentage",
                n."projected_growth_rate",
                b."growth_percentage_opvalue",
                b."projected_growth_rate_opvalue",
                b."fcastfairvalue",
                b."nextyrfcastfairvalue",
                n."quarterenddate",
                n."quarter",
                n."filingdate",
                n."earn_flag",
                n."div_flag",
                ROW_NUMBER() OVER (PARTITION BY n."seccode" ORDER BY n."quarterenddate" DESC, n."filingdate" DESC) AS rn
            FROM 
                "d_fins_all_netsales" n
            JOIN 
                filtered_seccode f ON n."seccode" = f."seccode"
            LEFT JOIN
                "d_fins_all_bps_opvalues" b
            ON
                n."seccode" = b."seccode" AND n."quarterenddate" = b."quarterenddate"
            WHERE 
                {where_conditions}
            GROUP BY 
                n."seccode", n."companyname", n."fiscalyearend", n."growth_percentage", n."projected_growth_rate", 
                b."growth_percentage_opvalue", b."projected_growth_rate_opvalue", b."fcastfairvalue", b."nextyrfcastfairvalue", 
                n."quarterenddate", n."quarter", n."filingdate", n."earn_flag", n."div_flag"
        )
        SELECT * FROM latest_records 
        WHERE rn = 1
        {start_date_condition}
        ORDER BY "seccode", "quarterenddate" DESC;
    """

    logging.debug("Constructed SQL Query:\n%s", query)

    try:
        with engine.connect() as conn:
            df = pd.read_sql(query, conn)
            logging.info("Rows returned: %d", df.shape[0])
            logging.debug("Sample rows:\n%s", df.head().to_string(index=False))

            df[['growth_percentage', 'projected_growth_rate', 'growth_percentage_opvalue', 'projected_growth_rate_opvalue']] = df[
                ['growth_percentage', 'projected_growth_rate', 'growth_percentage_opvalue', 'projected_growth_rate_opvalue']
            ].round(2)

            total_companies = pd.read_sql('SELECT COUNT(DISTINCT "seccode") FROM d_fins_all_netsales WHERE "companyname" != \'Unknown\'', conn).iloc[0, 0]
            filtered_companies_count = df['seccode'].nunique()

            if df.empty:
                logging.info("No filtered companies found, will render index.html")
            else:
                logging.info("Rendering filtered_results.html with %d records", len(df))
    except Exception as e:
        logging.error(f"Error executing query: {e}")
        df = pd.DataFrame()
        total_companies = 0
        filtered_companies_count = 0

    return df, filtered_companies_count, total_companies

