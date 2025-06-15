
# uweb_12/app.py
# === Standard Library Imports ===
import os
import logging
import threading
from datetime import datetime, timedelta
from io import BytesIO

# === Third-Party Imports ===
from flask import (
    Flask, render_template, request, redirect,
    url_for, flash, get_flashed_messages, Response
)
import pandas as pd
import matplotlib.pyplot as plt
from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
from dotenv import load_dotenv

# === Load Environment Variables ===
load_dotenv(dotenv_path='/mnt/c/Users/osamu/OneDrive/onedrive_python_source/envs/.env.uweb_12')

# Track rendering start times
RENDER_TIMING_TRACKER = {}

# === Local Application Imports ===
from application.backend.viewer_utils.viewer_auth import get_id_token
from application.backend.viewer_utils.viewer_fetch import fetch_weekly_margin_interest, fetch_company_name, fetch_short_selling_positions, fetch_daily_quotes
from application.backend.viewer_utils.chart_plotly import create_combined_chart

from application.backend.auth import login, logout, is_logged_in
from application.backend.fetch_company_data import fetch_filtered_companies
from application.backend.filtered_table import create_filtered_results_table, insert_filtered_results
from application.backend.db_select import engine, environment
from application.plot_fins_all_bps_opvalues import plot_combined_chart
from application.plot_fins_all_netsales import plot_qonq_growth

from application.routes.growth_route import growth_bp
from application.routes.recordhigh_route import recordhigh_bp
from application.routes.record_w52_high_route import record_w52_high_bp
from application.routes.value_route import value_bp
from application.routes.dividend_route import dividend_bp

# === Logging Configuration ===
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# === Flask App Initialization ===
app = Flask(__name__, template_folder='application/templates', static_folder='application/static')

# === Thread Safety ===
insert_lock = threading.Lock()

# === Blueprint Registration ===
app.register_blueprint(growth_bp, url_prefix='/growth')
app.register_blueprint(recordhigh_bp, url_prefix='/recordhigh')
app.register_blueprint(record_w52_high_bp, url_prefix='/record_w52_high')
app.register_blueprint(value_bp, url_prefix='/value')
app.register_blueprint(dividend_bp, url_prefix='/dividend')

app.secret_key = os.urandom(24)

@app.route('/login', methods=['GET', 'POST'])
def login_route():
    return login()

@app.route('/logout')
def logout_route():
    return logout()

# Utility function for safer data conversion
def get_request_param(name, default='0'):
    value = request.form.get(name, default)
    try:
        return float(value)
    except ValueError:
        flash(f"Invalid value for {name}. Defaulting to {default}.", "warning")
        return float(default)

@app.route('/plot/<seccode>')
def plot(seccode):
    source = request.args.get('source', 'index')

    logging.info("------------------------------------------------------------")
    logging.info("🟰" * 29)
    logging.info("🔽🔽🔽🔽🔽 NEW CHART RENDERING 🔽🔽🔽🔽🔽")
    logging.info(f"Started plotting chart for {seccode}")

    # Start total rendering timer
    RENDER_TIMING_TRACKER[seccode] = datetime.now()

    # Determine the table based on the source
    table_name = None
    if source == 'filtered_results':
        table_name = 'filtered_results'
    elif source == 'growth':
        table_name = 'growth'
    elif source == 'recordhigh':
        table_name = 'recordhigh'
    elif source == 'record_w52_high':
        table_name = 'record_w52_high'
    elif source == 'value':
        table_name = 'value'
    elif source == 'dividend':
        table_name = 'dividend'

    companyname = None
    next_seccode = None
    previous_seccode = None
    earn_flag = None
    div_flag = None

    if table_name:
        current_company_query = f"SELECT * FROM {table_name} WHERE seccode = :seccode"
        next_company_query = f"""
            SELECT seccode FROM {table_name}
            WHERE id = (SELECT MIN(id) FROM {table_name} WHERE id > 
                        (SELECT id FROM {table_name} WHERE seccode = :seccode))
        """
        previous_company_query = f"""
            SELECT seccode FROM {table_name}
            WHERE id = (SELECT MAX(id) FROM {table_name} WHERE id < 
                        (SELECT id FROM {table_name} WHERE seccode = :seccode))
        """
        with engine.connect() as conn:
            current_company = conn.execute(text(current_company_query), {"seccode": seccode}).fetchone()

            if current_company:
                current_company_dict = dict(current_company._mapping)
                companyname = current_company_dict.get('companyname')
                if source == 'filtered_results':
                    earn_flag = current_company_dict.get('earn_flag', '')
                    div_flag = current_company_dict.get('div_flag', '')
            next_seccode = conn.execute(text(next_company_query), {"seccode": seccode}).scalar()
            previous_seccode = conn.execute(text(previous_company_query), {"seccode": seccode}).scalar()

    data_found = False
    with engine.connect() as conn:
        bps_query = f"SELECT * FROM d_fins_all_bps_opvalues WHERE seccode = :seccode"
        netsales_query = f"SELECT * FROM d_fins_all_netsales WHERE seccode = :seccode"

        bps_data = conn.execute(text(bps_query), {"seccode": seccode}).fetchall()
        netsales_data = conn.execute(text(netsales_query), {"seccode": seccode}).fetchall()

        if bps_data or netsales_data:
            data_found = True

    # Generate plots or show a warning
    if data_found:
        try:
            img1, fetched_companyname = plot_combined_chart(seccode, engine)
            img2, _ = plot_qonq_growth(seccode, engine)
            if not companyname:
                companyname = fetched_companyname
        except Exception as e:
            logging.error(f"Error generating plots: {e}")
            img1, img2 = None, None
    else:
        flash(f"No data available in `d_fins_all_bps_opvalues` or `d_fins_all_netsales` for Sec Code: {seccode}.", "info")
        img1, img2 = None, None

    return render_template(
        'plot.html',
        seccode=seccode,
        companyname=companyname or "Company name not available",
        next_seccode=next_seccode,   # Restored navigation logic
        previous_seccode=previous_seccode,  # Restored navigation logic
        source=source,
        earn_flag=earn_flag,
        div_flag=div_flag,
        img1=img1,
        img2=img2
    )

@app.route('/plot_direct', methods=['POST'])
def plot_direct():
    seccode = request.form.get('seccode')
    source = request.form.get('source', 'index')  # Default to 'index' if not specified
    if not seccode:
        flash("No Sec Code provided.", "error")
        return redirect(url_for('filtered_results'))
    
    return redirect(url_for('plot', seccode=seccode, source=source))

@app.route('/plotly_chart/<seccode>')
def plotly_chart(seccode):
    try:
        id_token = get_id_token()
        df_margin = fetch_weekly_margin_interest(seccode, id_token)
        df_prices = fetch_daily_quotes(seccode, id_token)
        df_shorts = fetch_short_selling_positions(seccode, id_token)
        jq_companyname = fetch_company_name(seccode, id_token)

        if not df_prices.empty and not df_margin.empty:
            chart_html = create_combined_chart(
                df_prices, df_margin, df_shorts, jq_companyname or seccode
            )
        else:
            chart_html = "<p>Plotly chart could not be loaded.</p>"

    except Exception as e:
        logging.exception("Failed to render Plotly chart")
        chart_html = f"<p>Error rendering Plotly chart: {e}</p>"

    return chart_html

@app.route('/plot_image/<seccode>')
def plot_image(seccode):
    try:
        img1, companyname = plot_combined_chart(seccode, engine)
        img2, _ = plot_qonq_growth(seccode, engine)

        # Combine images
        img = combine_charts(img1, img2)

        # Log total rendering time
        started_at = RENDER_TIMING_TRACKER.pop(seccode, None)
        if started_at:
            total_time = (datetime.now() - started_at).total_seconds()
            logging.info(f"🧮 Total rendering time for {seccode}: {total_time:.2f} seconds.")

        return Response(img.getvalue(), mimetype='image/png')

    except Exception as e:
        logging.error(f"Failed to generate plot image for Sec Code: {seccode} due to {e}")
        return f"Failed to generate plot image for Sec Code: {seccode} due to {e}"

def combine_charts(img1, img2):
    fig = plt.figure(figsize=(18, 12))
    gs = plt.GridSpec(2, 1, height_ratios=[2, 1])

    ax1 = fig.add_subplot(gs[0])
    ax1.imshow(plt.imread(BytesIO(img1.getvalue())))
    ax1.axis('off')

    ax2 = fig.add_subplot(gs[1])
    ax2.imshow(plt.imread(BytesIO(img2.getvalue())))
    ax2.axis('off')

    plt.subplots_adjust(hspace=0)
    combined_img = BytesIO()
    plt.savefig(combined_img, format='png', bbox_inches='tight', pad_inches=0.02)
    plt.close()
    combined_img.seek(0)

    return combined_img

@app.route('/', methods=['GET', 'POST'])
def index():
    if not is_logged_in():
        logging.info("User not logged in, redirecting to login page.")
        return redirect(url_for('login_route'))

    no_data_found = False

    if request.method == 'POST':
        logging.info("Received POST request at index route.")
        try:
            # Parse input thresholds
            def parse_threshold(field_name):
                val = request.form.get(field_name)
                return None if val == 'N/A' else float(val)

            growth_percentage_threshold = parse_threshold('growth_percentage_threshold')
            projected_growth_rate_threshold = parse_threshold('projected_growth_rate_threshold')
            growth_percentage_opvalue_threshold = parse_threshold('growth_percentage_opvalue_threshold')
            projected_growth_rate_opvalue_threshold = parse_threshold('projected_growth_rate_opvalue_threshold')

            logging.debug("Thresholds: growth=%s, projected=%s, opvalue_growth=%s, opvalue_projected=%s",
              growth_percentage_threshold, projected_growth_rate_threshold,
              growth_percentage_opvalue_threshold, projected_growth_rate_opvalue_threshold)


            # Parse dates and filters
            # start_date = request.form.get('start_date') or (datetime.today() - timedelta(days=365)).strftime('%Y-%m-%d')
            start_date = request.form.get('start_date') or None
            filingdate = request.form.get('filingdate') or None
            data_years = request.form.get('data_years')
            data_years = None if data_years == 'N/A' else int(data_years)

            logging.info("Filters: start_date=%s, data_years=%s, filingdate=%s", start_date, data_years, filingdate)

            # Fetch filtered data
            try:
                filtered_companies, filtered_companies_count, total_companies = fetch_filtered_companies(
                    engine,
                    growth_percentage_threshold,
                    projected_growth_rate_threshold,
                    growth_percentage_opvalue_threshold,
                    projected_growth_rate_opvalue_threshold,
                    start_date,
                    data_years,
                    filingdate
                )
            except SQLAlchemyError as db_error:
                logging.exception("Database error during fetch_filtered_companies.")
                flash(f"Database error: {db_error}", "error")
                return render_template('index.html', no_data_found=True)

            if filtered_companies.empty:
                no_data_found = True
                logging.info("No matching records found. Displaying empty index page.")
                flash("No data found matching your criteria.", "info")
            else:
                # Use a lock to ensure only one insert operation at a time
                with insert_lock:
                    try:
                        logging.info("Acquired insert lock. Proceeding with table reset and insert.")
                        create_filtered_results_table(engine)
                        insert_filtered_results(engine, filtered_companies)
                        flash(f"{filtered_companies_count} records found and successfully saved.", "success")
                    except Exception as e:
                        logging.exception("Failed to insert filtered data.")
                        flash(f"Error inserting filtered data: {e}", "error")
                        return render_template('index.html', no_data_found=True)
    
            logging.info("Rendering filtered_results.html with %d companies.", filtered_companies_count)
            return render_template(
                'filtered_results.html',
                companies=filtered_companies.to_dict('records'),
                total_companies=total_companies,
                filtered_companies_count=filtered_companies_count,
                growth_percentage_threshold=growth_percentage_threshold,
                projected_growth_rate_threshold=projected_growth_rate_threshold,
                growth_percentage_opvalue_threshold=growth_percentage_opvalue_threshold,
                projected_growth_rate_opvalue_threshold=projected_growth_rate_opvalue_threshold,
                start_date=start_date,
                filingdate=filingdate,
                data_years=data_years if data_years else 'N/A',
                no_data_found=no_data_found
            )

        except Exception as e:
            logging.exception("Unhandled exception in index POST request.")
            flash(f"An unexpected error occurred: {e}", "error")
            return render_template('index.html', no_data_found=True)

    return render_template('index.html', no_data_found=no_data_found)

@app.context_processor
def inject_flashed_messages():
    return dict(get_flashed_messages=get_flashed_messages)

@app.route('/filtered_results', methods=['GET'])
def filtered_results():
    try:
        query = "SELECT * FROM filtered_results ORDER BY id ASC;"
        with engine.connect() as conn:
            filtered_companies = pd.read_sql(query, conn)

        filtered_companies.columns = filtered_companies.columns.str.lower()

    except Exception as e:
        logging.error(f"Error fetching filtered results: {e}")
        return "Error loading filtered results.", 500

    return render_template(
        'filtered_results.html',
        companies=filtered_companies.to_dict('records'),
        total_companies=filtered_companies['seccode'].nunique(),
        filtered_companies_count=len(filtered_companies),
        no_data_found=filtered_companies.empty
    )

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)

