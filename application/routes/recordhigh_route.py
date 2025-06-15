

from flask import Blueprint, request, jsonify, render_template
from sqlalchemy import text
import pandas as pd
from application.backend.db_select import engine, environment

# Blueprint for Portfolio
recordhigh_bp = Blueprint('recordhigh', __name__)

@recordhigh_bp.route('/recordhigh')
def view_recordhigh():
    query = 'SELECT * FROM "recordhigh" ORDER BY "seccode" ASC'
    with engine.connect() as conn:
        recordhigh_df = pd.read_sql(query, conn)
    return render_template('recordhigh.html', recordhigh=recordhigh_df.to_dict('records'))

@recordhigh_bp.route('/add_to_recordhigh', methods=['POST'])
# def add_to_recordhigh():
#     sec_code = request.form.get('seccode')
#     if not sec_code:
#         return jsonify({"message": "seccode is required"}), 400
#     query = """SELECT COUNT(1) FROM recordhigh WHERE "seccode" = :sec_code"""
#     try:
#         with engine.connect() as conn:
#             result = conn.execute(text(query), {"sec_code": sec_code})
#             count = result.scalar()
#             if count > 0:
#                 return jsonify({"message": f"Sec Code {sec_code} is already in the recordhigh."}), 200
#             company_details = pd.read_sql(
#                 """
#                 SELECT n."seccode", n."companyname", n."fiscalyearend", n."quarter",
#                        n."growth_percentage", n."projected_growth_rate",
#                        b."growth_percentage_opvalue", b."projected_growth_rate_opvalue",
#                        n."quarterenddate"
#                 FROM "d_fins_all_netsales" n
#                 LEFT JOIN "d_fins_all_bps_opvalues" b
#                 ON n."seccode" = b."seccode" AND n."quarterenddate" = b."quarterenddate"
#                 WHERE n."seccode" = %(sec_code)s
#                 ORDER BY n."quarterenddate" DESC
#                 LIMIT 1
#                 """,
#                 engine,
#                 params={"sec_code": sec_code},
#             )
#             if company_details.empty:
#                 return jsonify({"message": "Company not found"}), 404
#             recordhigh_df = pd.read_sql("SELECT * FROM recordhigh ORDER BY seccode ASC", conn).drop(columns=["id"], errors="ignore")
#             updated_recordhigh_df = pd.concat([recordhigh_df, company_details], ignore_index=True)
#             updated_recordhigh_df.sort_values(by="seccode", inplace=True)
#             with engine.begin() as conn:
#                 conn.execute(text("DELETE FROM recordhigh;"))
#                 updated_recordhigh_df.to_sql("recordhigh", conn, if_exists="append", index=False)
#         return jsonify({"message": f"Added {sec_code} to recordhigh"}), 200
#     except Exception as e:
#         return jsonify({"message": f"Error adding to RecorHigh: {e}"}), 500
def add_to_recordhigh():
    sec_code = request.form.get('seccode')
    if not sec_code:
        return jsonify({"message": "seccode is required"}), 400

    try:
        with engine.connect() as conn:
            query = text("SELECT COUNT(1) FROM recordhigh WHERE seccode = :sec_code")
            count = conn.execute(query, {"sec_code": sec_code}).scalar()
            if count > 0:
                return jsonify({"message": f"Sec Code {sec_code} is already in the recordhigh."}), 200

            company_query = text("""
                SELECT n.seccode, n.companyname, n.fiscalyearend, n.quarter,
                       n.growth_percentage, n.projected_growth_rate,
                       b.growth_percentage_opvalue, b.projected_growth_rate_opvalue,
                       n.quarterenddate
                FROM d_fins_all_netsales n
                LEFT JOIN d_fins_all_bps_opvalues b
                ON n.seccode = b.seccode AND n.quarterenddate = b.quarterenddate
                WHERE n.seccode = :sec_code
                ORDER BY n.quarterenddate DESC
                LIMIT 1
            """)
            company_data = pd.read_sql(company_query, conn, params={"sec_code": sec_code})

            if company_data.empty:
                return jsonify({"message": "Company not found"}), 404

        insert_query = text("""
            INSERT INTO recordhigh (seccode, companyname, fiscalyearend, quarter, growth_percentage,
                                    projected_growth_rate, growth_percentage_opvalue, projected_growth_rate_opvalue,
                                    quarterenddate)
            VALUES (:seccode, :companyname, :fiscalyearend, :quarter, :growth_percentage,
                    :projected_growth_rate, :growth_percentage_opvalue, :projected_growth_rate_opvalue,
                    :quarterenddate)
            ON CONFLICT (seccode) DO NOTHING
        """)

        with engine.begin() as conn:
            conn.execute(insert_query, company_data.to_dict(orient="records")[0])

        return jsonify({"message": f"Added {sec_code} to recordhigh"}), 200

    except Exception as e:
        return jsonify({"message": f"Error adding to RecorHigh: {e}"}), 500

@recordhigh_bp.route('/remove_from_recordhigh', methods=['POST'])
def remove_from_recordhigh():
    seccode = request.form.get('seccode')
    if not seccode:
        return jsonify({"message": "SecCode is required"}), 400
    try:
        with engine.begin() as conn:
            result = conn.execute(text('DELETE FROM "recordhigh" WHERE "seccode" = :seccode'), {"seccode": seccode})
            rows_affected = result.rowcount
        if rows_affected > 0:
            return jsonify({"message": f"Removed record with SecCode {seccode} from RecorHigh"}), 200
        else:
            return jsonify({"message": f"Record with SecCode {seccode} not found in RecorHigh"}), 404
    except Exception as e:
        return jsonify({"message": f"Error removing from RecorHigh: {e}"}), 500