
can you make a code that do the following?
Access Jquants api and get histtorical stock prices and weekly_margin_interest.
Draw graph which consists of daily stock price bar charts, candle stick or ohlc, and line which shows weekly_margin_interest.
The graph has two parts upper portion shows stock charts, and the bottom portion shows. Or they can be combined.
time fram of the graph is 3 years long.
Stock price data will be fetched every time the charts is depict, but weekly_margin_interest data should be saved in table "weekly_margin_interest" in the folloing DB, and depicted from woth using that data.
mk table logic is needed if table does not exist. 
Databese selection logic is necessary.
This will be developed by Flask app.
indexx page will have box where company code will be probided and a grapf for that company will be rendered.
Is there any necessary info ? Or any Questions?

DB credentials:
HEROKU_DATABASE_URL=postgres://u4gfsf6lr4e5sj:p37e834285e1c5161de955adf23c5304df5878d00cb78847100ffac916c995840@ceqbglof0h8enj.cluster-czrs8kj4isg7.us-east-1.rds.amazonaws.com:5432/d1kmc11fnhb6np
LOCAL_DB_URL=postgresql://postgres_ubuntu:55@localhost:5432/postgres_ubuntu_db

API references:
G_MAIL_ADDRESS=o.fukushi@gmail.com
J_QUANTS_PASSWORD=7HKhUci36SBk4qX

Refresh token can be obtained using your registered email and password.
{
    "refreshToken": "<YOUR refreshToken>" 
}
import requests
import json

data={"mailaddress":"<YOUR EMAIL_ADDRESS>", "password":"<YOUR PASSWORD>"}
r_post = requests.post("https://api.jquants.com/v1/token/auth_user", data=json.dumps(data))
r_post.json()

The ID token can be obtained using the refresh token obtained on the sign in page.
{
    "idToken": "<YOUR idToken>" 
}
import requests
import json

REFRESH_TOKEN = "YOUR refreshtokenID"
r_post = requests.post(f"https://api.jquants.com/v1/token/auth_refresh?refreshtoken={REFRESH_TOKEN}")
r_post.json()

Listed Issue Information (/listed/info)
You can get information on listed companies and sector information
{
    "info": [
        {
            "Date": "2022-11-11",
            "Code": "86970",
            "CompanyName": "日本取引所グループ",
        　　　　　　　　"CompanyNameEnglish": "Japan Exchange Group,Inc.",
            "Sector17Code": "16",
            "Sector17CodeName": "金融（除く銀行）",
            "Sector33Code": "7200",
            "Sector33CodeName": "その他金融業",
            "ScaleCategory": "TOPIX Large70",
            "MarketCode": "0111",
            "MarketCodeName": "プライム",
            "MarginCode": "1",
            "MarginCodeName": "信用",
        }
    ]
}
import requests
import json

idToken = "YOUR idToken"
headers = {'Authorization': 'Bearer {}'.format(idToken)}
r = requests.get("https://api.jquants.com/v1/listed/info", headers=headers)
r.json()



Historical stock prices including both adjusted and unadjusted prices, taking into account stock splits, etc.
Stock price consists before and after adjustment of stock splits and reverse stock splits (Rounded to first decimal places)
Attention
    Open, High, low, close, the volume of trade and the amount of purchase for the issue on the day when there is no trade volume (no sale) are recorded as Null.
    Stocks that are not listed on the TSE (including issue listed only on the other exchanges) are not included in the data.
    The data for Oct. 1st, 2020 are the OHLC, trading volume, and trading value in Null because trading was halted all day due to the failure of the equity trading system, arrowhead.
    Daily prices can be obtained for all plans, but morning/afternoon session prices are available only for premium plan.
    Stock price adjustments are supported only for stock splits and reverse stock splits. Please note that some corporate actions are not supported.
{
    "daily_quotes": [
        {
            "Date": "2023-03-24",
            "Code": "86970",
            "Open": 2047.0,
            "High": 2069.0,
            "Low": 2035.0,
            "Close": 2045.0,
            "UpperLimit": "0",
            "LowerLimit": "0",
            "Volume": 2202500.0,
            "TurnoverValue": 4507051850.0,
            "AdjustmentFactor": 1.0,
            "AdjustmentOpen": 2047.0,
            "AdjustmentHigh": 2069.0,
            "AdjustmentLow": 2035.0,
            "AdjustmentClose": 2045.0,
            "AdjustmentVolume": 2202500.0,
            "MorningOpen": 2047.0,
            "MorningHigh": 2069.0,
            "MorningLow": 2040.0,
            "MorningClose": 2045.5,
            "MorningUpperLimit": "0",
            "MorningLowerLimit": "0",
            "MorningVolume": 1121200.0,
            "MorningTurnoverValue": 2297525850.0,
            "MorningAdjustmentOpen": 2047.0,
            "MorningAdjustmentHigh": 2069.0,
            "MorningAdjustmentLow": 2040.0,
            "MorningAdjustmentClose": 2045.5,
            "MorningAdjustmentVolume": 1121200.0,
            "AfternoonOpen": 2047.0,
            "AfternoonHigh": 2047.0,
            "AfternoonLow": 2035.0,
            "AfternoonClose": 2045.0,
            "AfternoonUpperLimit": "0",
            "AfternoonLowerLimit": "0",
            "AfternoonVolume": 1081300.0,
            "AfternoonTurnoverValue": 2209526000.0,
            "AfternoonAdjustmentOpen": 2047.0,
            "AfternoonAdjustmentHigh": 2047.0,
            "AfternoonAdjustmentLow": 2035.0,
            "AfternoonAdjustmentClose": 2045.0,
            "AfternoonAdjustmentVolume": 1081300.0
        }
    ],
    "pagination_key": "value1.value2."
}
import requests
import json

idToken = "YOUR idToken"
headers = {'Authorization': 'Bearer {}'.format(idToken)}
r = requests.get("https://api.jquants.com/v1/prices/daily_quotes?code=86970&date=20230324", headers=headers)
r.json()

Margin Trading Outstandings (/markets/weekly_margin_interest)
Weekly margin trading outstandings is available.
{
    "weekly_margin_interest": [
        {
            "Date": "2023-02-17",
            "Code": "13010",
            "ShortMarginTradeVolume": 4100.0,
            "LongMarginTradeVolume": 27600.0,
            "ShortNegotiableMarginTradeVolume": 1300.0,
            "LongNegotiableMarginTradeVolume": 7600.0,
            "ShortStandardizedMarginTradeVolume": 2800.0,
            "LongStandardizedMarginTradeVolume": 20000.0,
            "IssueType": "2"
        }
    ],
    "pagination_key": "value1.value2."
}
import requests
import json

idToken = "YOUR idToken"
headers = {'Authorization': 'Bearer {}'.format(idToken)}
r = requests.get("https://api.jquants.com/v1/markets/weekly_margin_interest?code=86970", headers=headers)
r.json()

Outstanding Short Selling Positions Reported (/markets/short_selling_positions)
You can get the outstanding short selling positions reported data.
{
    "short_selling_positions": [
      {
        "DisclosedDate": "2024-08-01",
        "CalculatedDate": "2024-07-31",
        "Code": "13660",
        "ShortSellerName": "個人",
        "ShortSellerAddress": "",
        "DiscretionaryInvestmentContractorName": "",
        "DiscretionaryInvestmentContractorAddress": "",
        "InvestmentFundName": "",
        "ShortPositionsToSharesOutstandingRatio": 0.0053,
        "ShortPositionsInSharesNumber": 140000,
        "ShortPositionsInTradingUnitsNumber": 140000,
        "CalculationInPreviousReportingDate": "2024-07-22",
        "ShortPositionsInPreviousReportingRatio": 0.0043,
        "Notes": ""
      }
    ],
    "pagination_key": "value1.value2."
}
import requests
import json

idToken = "YOUR idToken"
headers = {'Authorization': 'Bearer {}'.format(idToken)}
r = requests.get("https://api.jquants.com/v1/markets/short_selling_positions?code=86970&calculated_date=20240801", headers=headers)
r.json()

can we combine the following two projects and show the following graphes on the same plot page when called by their seccode?
they use the same api to get data and draw graphs based on fetched data. they also draw overlay stock price chart to that graps. chart view get stock price data from api, but uweb12 gets those fron yfinance.
chart_viewer:
project/
├── .gitignore
├── app.py
├── Dockerfile
├── Procfile
├── README.md
├── requirements.txt
├── runtime.txt
├── templates/
|        └── index.html
└── utils/
       ├── auth.py
       └── fetch.py
# utils/auth.py

import os
import logging
import requests
import json

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')

# Load credentials from env
JQ_USER = os.getenv("G_MAIL_ADDRESS")
JQ_PASS = os.getenv("J_QUANTS_PASSWORD")

def get_refresh_token() -> str:
    """Fetch refresh token using email and password."""
    data = {"mailaddress": JQ_USER, "password": JQ_PASS}
    res = requests.post(
        "https://api.jquants.com/v1/token/auth_user",
        data=json.dumps(data)
    )
    if res.status_code != 200 or "refreshToken" not in res.json():
        logging.error("Failed to get refresh token: %s", res.text)
        return None
    return res.json()["refreshToken"]

from time import sleep

def get_id_token(retries=3) -> str:
    for attempt in range(retries):
        refresh_token = get_refresh_token()
        if not refresh_token:
            continue
        res = requests.post(
            f"https://api.jquants.com/v1/token/auth_refresh?refreshtoken={refresh_token}"
        )
        if res.status_code == 200 and "idToken" in res.json():
            return res.json()["idToken"]
        logging.warning("Retrying ID token fetch... (%d/%d)", attempt + 1, retries)
        sleep(1)
    logging.error("Failed to get ID token after retries.")
    return None

# utils/margin.py

import os
import logging
import pandas as pd
import requests
import datetime as dt

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')

# ENV VARS
JQ_USER = os.getenv("G_MAIL_ADDRESS")
JQ_PASS = os.getenv("J_QUANTS_PASSWORD")

DEFAULT_YEARS = int(os.getenv("FETCH_YEARS", 3))

def fetch_daily_quotes(code, id_token, years: int = DEFAULT_YEARS):
    today = dt.date.today()
    from_date = today - dt.timedelta(days=365 * years)
    headers = {'Authorization': f'Bearer {id_token}'}
    url = f"https://api.jquants.com/v1/prices/daily_quotes?code={code}&from={from_date.strftime('%Y-%m-%d')}"
    r = requests.get(url, headers=headers)
    df = pd.DataFrame(r.json().get("daily_quotes", []))
    logging.info("Daily quote data retrieved from API:\n%s", df.tail())
    return df

def fetch_weekly_margin_interest(code, id_token, years: int = DEFAULT_YEARS):
    headers = {'Authorization': f'Bearer {id_token}'}
    from_date = dt.date.today() - dt.timedelta(days=365 * years)
    url = f"https://api.jquants.com/v1/markets/weekly_margin_interest?code={code}&from={from_date.strftime('%Y-%m-%d')}"
    r = requests.get(url, headers=headers)
    df = pd.DataFrame(r.json().get("weekly_margin_interest", []))

    if df.empty:
        logging.warning("No margin interest data returned from API for code: %s", code)
        return pd.DataFrame(columns=["Date", "Code", "ShortMarginTradeVolume", "LongMarginTradeVolume"])

    df = df[["Date", "Code", "ShortMarginTradeVolume", "LongMarginTradeVolume"]]
    df["ScaledShortMargin"] = df["ShortMarginTradeVolume"] / 1000
    df["ScaledLongMargin"] = df["LongMarginTradeVolume"] / 1000
    logging.info("Margin data retrieved from API:\n%s", df.tail())
    return df

def fetch_company_name(code, id_token):
    headers = {'Authorization': f'Bearer {id_token}'}
    url = "https://api.jquants.com/v1/listed/info"
    r = requests.get(url, headers=headers)
    info = r.json().get("info", [])
    df = pd.DataFrame(info)

    if df.empty or code not in df['Code'].values:
        logging.warning("No company info found for code: %s", code)
        return None

    name = df.loc[df['Code'] == code, 'CompanyName'].values[0].strip()
    logging.info("Company name for %s is %s", code, name)
    return name

def fetch_short_selling_positions(code, id_token, years: int = DEFAULT_YEARS):
    headers = {'Authorization': f'Bearer {id_token}'}
    from_date = dt.date.today() - dt.timedelta(days=365 * years)
    params = f"?code={code}&from={from_date.strftime('%Y-%m-%d')}"
    url = f"https://api.jquants.com/v1/markets/short_selling_positions{params}"
    r = requests.get(url, headers=headers)
    df = pd.DataFrame(r.json().get("short_selling_positions", []))

    if df.empty:
        logging.warning("No short selling data returned from API for code: %s", code)
        return pd.DataFrame(columns=[
            "DisclosedDate", "CalculatedDate", "Code", "ShortSellerName",
            "InvestmentFundName", "DiscretionaryInvestmentContractorName",
            "ShortPositionsToSharesOutstandingRatio", "ShortPositionsInSharesNumber"
        ])

    df = df[[
        "DisclosedDate", "CalculatedDate", "Code", "ShortSellerName",
        "InvestmentFundName", "DiscretionaryInvestmentContractorName",
        "ShortPositionsToSharesOutstandingRatio", "ShortPositionsInSharesNumber"
    ]]

    df["CalculatedDate"] = pd.to_datetime(df["CalculatedDate"])
    df = df[df["CalculatedDate"].dt.date >= from_date]
    df["ScaledShortShares"] = df["ShortPositionsInSharesNumber"] / 1000

    logging.info("Short selling data retrieved from API:\n%s", df[[
        "CalculatedDate", "ShortSellerName", "InvestmentFundName",
        "DiscretionaryInvestmentContractorName", "ScaledShortShares"
    ]].tail())

    return df



# chart_viewer/app.py

import os
import json
import datetime as dt
import logging
from flask import Flask, render_template, request
import psycopg2
import requests
import pandas as pd
import plotly.graph_objs as go
from urllib.parse import urlparse
from dotenv import load_dotenv
load_dotenv(dotenv_path="/mnt/c/Users/osamu/OneDrive/onedrive_python_source/envs/.env.chart_viwer")
from utils.auth import get_id_token
from utils.fetch import (
    fetch_weekly_margin_interest,
    fetch_company_name,
    fetch_short_selling_positions,
    fetch_daily_quotes
)

# Setup logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s: %(message)s')

app = Flask(__name__)

def plot_candlestick(df_prices):
    return go.Candlestick(
        x=df_prices['Date'],
        open=df_prices['AdjustmentOpen'],
        high=df_prices['AdjustmentHigh'],
        low=df_prices['AdjustmentLow'],
        close=df_prices['AdjustmentClose'],
        name='Stock Price'
    )

def plot_long_margin(df_margin):
    return go.Bar(
        x=df_margin['Date'],
        y=df_margin['ScaledLongMargin'],
        name='Long Margin Volume',
        yaxis='y2',
        marker_color='blue',
        opacity=0.7
    )

def plot_short_margin(df_margin):
    return go.Bar(
        x=df_margin['Date'],
        y=df_margin['ScaledShortMargin'],
        name='Short Margin Volume',
        yaxis='y2',
        marker_color='red',
        opacity=0.7
    )

def plot_short_selling_positions(df_shorts):
    if df_shorts is None or df_shorts.empty or 'ScaledShortShares' not in df_shorts.columns:
        logging.warning("No valid short selling data to plot.")
        return []
    return go.Scatter(
        x=df_shorts["CalculatedDate"],
        y=df_shorts["ScaledShortShares"],
        mode='lines+markers',
        name="Outstanding Short Positions",
        yaxis="y2",
        line=dict(color='darkorange', width=2, dash='dot')
    )

def create_combined_chart(df_prices, df_margin, df_shorts, company_name):
    df_prices['Date'] = pd.to_datetime(df_prices['Date'])
    df_margin['Date'] = pd.to_datetime(df_margin['Date'])

    df_margin['ScaledShortMargin'] = df_margin['ShortMarginTradeVolume'] / 1000
    df_margin['ScaledLongMargin'] = df_margin['LongMarginTradeVolume'] / 1000

    if df_shorts is not None and not df_shorts.empty and 'CalculatedDate' in df_shorts.columns:
        df_shorts['CalculatedDate'] = pd.to_datetime(df_shorts['CalculatedDate'])

    traces = [
        plot_candlestick(df_prices),
        plot_long_margin(df_margin),
        plot_short_margin(df_margin)
    ]

    short_plot = plot_short_selling_positions(df_shorts)
    if short_plot:
        traces.append(short_plot)

    fig = go.Figure(data=traces)

    fig.update_layout(
        title=f'Stock Price & Margin Interest for {company_name}' if company_name else 'Stock Price & Margin Interest',
        xaxis={'title': 'Date'},
        yaxis={'title': 'Price'},
        yaxis2={
            'title': 'Margin / Short Vol. (×1,000)',
            'overlaying': 'y',
            'side': 'right'
        },
        height=750,
        width=None,  # Let HTML/CSS handle width
        autosize=True, 
        barmode='overlay'
    )

    return fig.to_html(full_html=False)

# Flask Views
@app.route('/', methods=['GET', 'POST'])
def index():
    chart_html = ""
    company_name = ""
    error_message = ""

    if request.method == 'POST':
        raw_code = request.form['code'].strip()
        code = raw_code if len(raw_code) == 5 else raw_code + "0"

        id_token = get_id_token()

        df_margin = fetch_weekly_margin_interest(code, id_token)
        df_prices = fetch_daily_quotes(code, id_token)
        df_shorts = fetch_short_selling_positions(code, id_token)
        company_name = fetch_company_name(code, id_token)

        if df_prices.empty or df_margin.empty:
            error_message = f"データが見つかりませんでした: 証券コード {raw_code} を確認してください。"
        else:
            chart_html = create_combined_chart(df_prices, df_margin, df_shorts, company_name or raw_code)

    return render_template('index.html', chart=chart_html, company_name=company_name, error_message=error_message)

if __name__ == '__main__':
    app.run(debug=True)

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Stock Price and Margin Chart</title>
    <script src="https://cdn.plot.ly/plotly-latest.min.js"></script>
    <style>
        body {
            font-family: Arial, sans-serif;
            /* max-width: 1000px; */
            margin: 2rem auto;
            padding: 1rem;
            max-width: none; /* Remove the 1000px limit */
        }
        #chart {
        width: 100%;
        }
        form {
            margin-bottom: 2rem;
        }
        label {
            font-weight: bold;
            margin-right: 0.5rem;
        }
        input[type="text"] {
            padding: 0.5rem;
            width: 200px;
        }
        button {
            padding: 0.5rem 1rem;
        }
    </style>
</head>
<body>
    <h1>JQuants Stock Chart Viewer</h1>
    <form method="POST">
        <label for="code">Enter Stock Code:</label>
        <input type="text" name="code" id="code" 
               value="{{ request.form['code'] if request.method == 'POST' else '' }}" 
               required>
        <button type="submit">Render Chart</button>
    </form>

    {% if company_name %}
    <h2>{{ company_name }} ({{ request.form['code'] }})</h2>
    {% endif %}

    {% if chart %}
        <div id="chart">{{ chart|safe }}</div>
    {% else %}
        <p style="color: red;">No chart available. Please check the stock code or try again later.</p>
    {% endif %}
    {% if error %}
    <div style="color: red; font-weight: bold;">{{ error }}</div>
    {% endif %}
    {% if error_message %}
    <div class="alert alert-danger">{{ error_message }}</div>
    {% endif %}


</body>
</html>
   

uweb_12:
project/
├── .env
├── .gitignore
├── app.py
├── Dockerfile
├── Procfile
├── README.md
├── requirements.txt
└── application/
       ├── backend/
       |      ├── __init__.py
       |      ├── auth.py
       |      ├── db_select.py
       |      ├── fetch_company_data.py
       |      ├── filtered_table.py     
       |      └── stock_price.py  
       ├── fonts/
       ├── routes/
       |      ├── __init__.py
       |      ├── dividend_route.py
       |      ├── growth_route.py
       |      ├── record_w52_high_route.py
       |      ├── recordhigh_route.py
       |      └── value_route.py
       ├── static/
       |      ├── css/
       |      ├── js/
       |      └── images/
       ├── templates/
       |       ├── dividend.html
       |       ├── filtered_results.html
       |       ├── growth.html
       |       ├── index.html
       |       ├── login.html
       |       ├── plot.html
       |       ├── record_w52_high.html
       |       ├── recordhigh.html
       |       └── value.html
       ├── __init__.py
       ├── plot_fins_all_bps_opvalues.py
       ├── plot_fins_all_netsales.py


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
load_dotenv(dotenv_path='/mnt/c/Users/osamu/OneDrive/onedrive_python_source/envs/.env.uweb_11')

# Track rendering start times
RENDER_TIMING_TRACKER = {}

# === Local Application Imports ===
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

# uewb_12/auth.py
import os
from flask import session, redirect, url_for, render_template, request, flash
from werkzeug.security import check_password_hash, generate_password_hash
from dotenv import load_dotenv

# Load the .env file
load_dotenv(dotenv_path='/mnt/c/Users/osamu/OneDrive/onedrive_python_source/envs/.env.uweb_11')

# Fetch email and password from environment variables
EMAIL = os.getenv('G_MAIL_ADDRESS')
PASSWORD = os.getenv('UMINEKO_FUND_PASSWORD')

# Hash the password from the .env file
hashed_password = generate_password_hash(PASSWORD)

# Dummy user credentials fetched from environment variables
users = {
    EMAIL: {
        "password": hashed_password
    }
}

# Function to check if the user is logged in
def is_logged_in():
    return 'user' in session

# Login logic
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        user = users.get(email)
        if user and check_password_hash(user['password'], password):
            session['user'] = email  # Store the email in the session
            return redirect(url_for('index'))
        else:
            flash('Invalid credentials. Please try again.')

    return render_template('login.html')

# Logout logic
def logout():
    session.pop('user', None)  # Remove the user from the session
    return redirect(url_for('login'))


# uweb_12/db_select.py

import os
from sqlalchemy import create_engine
from dotenv import load_dotenv

def get_database_engine():
    load_dotenv(dotenv_path='/mnt/c/Users/osamu/OneDrive/onedrive_python_source/envs/.env.uweb_11')
    
    # Detect environment
    is_heroku = os.getenv("HEROKU_ENV", "false").lower() == "true"
    is_render = os.getenv("RENDER_ENV", "false").lower() == "true"
    is_local = not is_heroku and not is_render

    if is_heroku:
        db_url = os.getenv('HEROKU_DATABASE_URL')
        environment = "Heroku"
    elif is_render:
        db_url = os.getenv('RENDER_DATABASE_URL') 
        # For Local Testing purposes
        # db_url = os.getenv('External_RENDER_DATABASE_URL') 
        environment = "Render"
    else:
        db_url = os.getenv('LOCAL_DB_URL')
        environment = "Local"

    if not db_url:
        raise ValueError("No database URL found in environment variables.")
    
    db_url = db_url.replace('postgres://', 'postgresql+psycopg2://')

    # Create engine with connection pooling
    engine = create_engine(
        db_url,
        pool_size=10,           # Base pool size
        max_overflow=5,          # Max extra connections if pool is full
        pool_timeout=30,         # Timeout to get connection
        pool_recycle=1800,        # Recycle connections every 30 minutes
        pool_pre_ping=True  # ✅ Add this to auto-check if connection is alive
    )
    return engine, environment

engine, environment = get_database_engine()


<!-- /* uweb_12/plot.html */ -->

<!DOCTYPE html>
<html>
<head>
    <title>Graph for {{ companyname }}</title>
    <style>
        .title-container {
            display: flex; /* Arranges the items in a row */
            justify-content: center; /* Centers the items horizontally */
            align-items: center; /* Aligns items vertically */
            gap: 20px; /* Adds spacing between the items */
            margin-top: 20px; /* Optional: Adds space from the top */
        }
    
        .title-container h1 {
            margin: 0; /* Removes default margin */
            font-size: 2em; /* Adjust font size as needed */
        }
    
        .title-container h2 {
            margin: 0; /* Removes default margin */
            font-size: 1.5em; /* Adjust font size as needed */
            color: #555; /* Optional: Change color for distinction */
        }
    </style>
    
    <style>
        body {
            font-family: Arial, sans-serif;
            background-color: #f0f0f0;
            text-align: center;
            margin: 0;
            padding: 0;
        }
        .header {
            margin-top: 20px;
            margin-bottom: 20px;
        }

        .graph-container {
            margin: 20px auto;
            padding: 10px;
            background-color: white;
            border: 1px solid #ccc;
            width: 80%;
            box-shadow: 0px 0px 10px rgba(0,0,0,0.1);
            position: relative;
            text-align: center;
        }
        #graph-img {
            display: block;
            margin: 0 auto;
            max-width: 100%;
            height: auto;
        }
        .return-button {
            margin-top: 20px;
        }
        .return-button a {
            text-decoration: none;
            color: white;
            background-color: #4CAF50;
            padding: 10px 20px;
            border-radius: 5px;
            font-size: 1em;
        }
        .return-button a:hover {
            background-color: #45a049;
        }
        #loading {
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            font-size: 1.2em;
            color: #555;
        }
        /* General button styles */
        .growth-button,
        .recordhigh-button,
        .value-button,
        .record-w52-button,
        .dividend-button {
            padding: 10px 20px;
            border-radius: 5px;
            font-size: 1em;
            border: none;
            cursor: pointer;
            color: white;
            margin: 5px; /* Add spacing between buttons */
        }

        /* Growth button styles */
        .growth-button {
            background-color: #007bff;
        }
        .growth-button:hover {
            background-color: #0056b3;
        }

        /* Portfolio button styles */
        .recordhigh-button {
            background-color: #ff4c4c;
        }
        .recordhigh-button:hover {
            background-color: #cc0000;
        }

        /* Value button styles */
        .value-button {
            background-color: #6a1b9a;
        }
        .value-button:hover {
            background-color: #4a148c;
        }

        /* Record W52 High button styles */
        .record-w52-button {
            background-color: #28a745;
        }
        .record-w52-button:hover {
            background-color: #218838;
        }
        .dividend-button {
            background-color: #ffa500;
        }
        .dividend-button:hover {
            background-color: #cc8400;
        }
    </style>
    <style>
        .additional-info {
            margin: 20px auto;
            text-align: center;
        }
        .additional-info table {
            margin: 0 auto;
            border-collapse: collapse;
        }
        .additional-info th, .additional-info td {
            border: 1px solid #ddd;
            padding: 8px;
        }
        .additional-info th {
            background-color: #f4f4f4;
        }
    </style>
    
    <script src="https://code.jquery.com/jquery-3.6.0.min.js"></script>
</head>
<body>
    <div class="title-container">
        <h1>Graph for {{ companyname }}</h1>
        <h2>Sec Code: {{ seccode }}</h2>
    </div>
    <div class="navigation-buttons">
        {% if source == 'index' %}
            <a href="{{ url_for('index') }}" class="button">Go to Index</a>
        {% elif source == 'growth' %}
            <a href="{{ url_for('growth.view_growth') }}" class="button">Go to Growth</a>
        {% elif source == 'value' %}
            <a href="{{ url_for('value.view_value') }}" class="button">Go to Value</a>
        {% elif source == 'recordhigh' %}
            <a href="{{ url_for('recordhigh.view_recordhigh') }}" class="button">Go to Record High</a>
        {% elif source == 'record_w52_high' %}
            <a href="{{ url_for('record_w52_high.record_w52_high') }}" class="button">Go to Record W52 High</a>
        {% elif source == 'dividend' %}
            <a href="{{ url_for('dividend.view_dividend') }}" class="button">Go to Dividend</a>
        {% elif source == 'filtered_results' %}
            <a href="{{ url_for('filtered_results') }}" class="button">Go to Filtered Results</a>
        {% endif %}

        {% if previous_seccode %}
            <a href="{{ url_for('plot', seccode=previous_seccode, source=source) }}" class="button">Previous</a>
        {% endif %}
        {% if next_seccode %}
            <a href="{{ url_for('plot', seccode=next_seccode, source=source) }}" class="button">Next</a>
        {% endif %}
        {% if not previous_seccode and not next_seccode %}
            <a href="javascript:history.back()" class="button">Go Back</a>
        {% endif %}
    </div>
    
    <!-- Revisions info for filtered_results -->
    {% if source == 'filtered_results' %}
    <div class="additional-info">
        <!-- <h3>Rivisions</h3> -->
        <table>
            <tr>
                <th>Earn Flag</th>
                <td>{{ earn_flag if earn_flag else '-' }}</td>
            </tr>
            <tr>
                <th>Div Flag</th>
                <td>{{ div_flag if div_flag else '-' }}</td>
            </tr>
        </table>
    </div>
    {% endif %}
    
    <div class="external-links">
        <a href="https://kabutan.jp/stock/finance?code={{ seccode }}" target="_blank">Kabutan</a>
        <a href="https://shikiho.toyokeizai.net/stocks/{{ seccode }}" target="_blank">四季報</a>
        <a href="https://www.tradingview.com/chart/?symbol=TSE:{{ seccode }}" target="_blank">Chart</a>
    </div>
    
    <div class="graph-container">
        <div id="loading">Loading...</div>
        <img id="graph-img" src="{{ url_for('plot_image', seccode=seccode) }}" alt="Graph for {{ companyname }}" style="display: none;">
    </div>
    
    <div class="button-container">
        {% if source == 'growth' %}
            <button class="growth-button" onclick="removeFromGrowth('{{ seccode }}')">Remove from Growth</button>
        {% else %}
            <button class="growth-button" onclick="addToGrowth('{{ seccode }}')">Add to Growth</button>
        {% endif %}

        {% if source == 'value' %}
        <button class="value-button" onclick="removeFromValue('{{ seccode }}')">Remove from Value</button>
        {% else %}
        <button class="value-button" onclick="addToValue('{{ seccode }}')">Add to Value</button>
        {% endif %}

        {% if source == 'recordhigh' %}
            <button class="recordhigh-button" onclick="removeFromRecordhigh('{{ seccode }}')">Remove from Record High</button>
        {% else %}
            <button class="recordhigh-button" onclick="addToRecordhigh('{{ seccode }}')">Add to Record High</button>
        {% endif %}

        {% if source == 'dividend' %}
            <button class="dividend-button" onclick="removeFromDividend('{{ seccode }}')">Remove from Dividend</button>
        {% else %}
            <button class="dividend-button" onclick="addToDividend('{{ seccode }}')">Add to Dividend</button>
        {% endif %}

        {% if source == 'record_w52_high' %}
            <button class="record-w52-button" onclick="removeFromRecordW52High('{{ seccode }}')">Remove from Record W52 High</button>
        {% endif %}
    </div>    

    <script>
        const img = document.getElementById('graph-img');
        const loading = document.getElementById('loading');
        
        img.onload = function() {
            loading.style.display = 'none';
            img.style.display = 'block';
        };
        
        img.onerror = function() {
            loading.innerHTML = 'Failed to load graph.';
        };
        
        function addToGrowth(seccode) {
            $.post("{{ url_for('growth.add_to_growth') }}", { seccode }, function(response) {
                alert(response.message);
            });
        }

        function removeFromGrowth(seccode) {
            $.post("{{ url_for('growth.remove_from_growth') }}", { seccode }, function(response) {
                alert(response.message);
            });
        }
        function addToValue(seccode) {
            $.post("{{ url_for('value.add_to_value') }}", { seccode }, function(response) {
                alert(response.message);
            });
        }
        function removeFromValue(seccode) {
            $.post("{{ url_for('value.remove_from_value') }}", { seccode }, function(response) {
                alert(response.message);
            });
        }
        function addToRecordhigh(seccode) {
            $.post("{{ url_for('recordhigh.add_to_recordhigh') }}", { seccode }, function(response) {
                alert(response.message);
            });
        }
        function removeFromRecordhigh(seccode) {
            $.post("{{ url_for('recordhigh.remove_from_recordhigh') }}", { seccode }, function(response) {
                alert(response.message);
            });
        }
        function removeFromRecordW52High(seccode) {
            $.post("{{ url_for('record_w52_high.remove_from_record_w52_high') }}", { seccode }, function(response) {
                alert(response.message);
            });
        }
        function addToDividend(seccode) {
            $.post("{{ url_for('dividend.add_to_dividend') }}", { seccode }, function(response) {
                alert(response.message);
            }).fail(function() {
                alert('Error adding to Dividend.');
            });
        }

        function removeFromDividend(seccode) {
            $.post("{{ url_for('dividend.remove_from_dividend') }}", { seccode }, function(response) {
                alert(response.message);
            }).fail(function() {
                alert('Error removing from Dividend.');
            });
        }
    </script>
</body>
</html>


# uweb_12/plot_fins_all_bps_opvalues.py

# === Standard Library Imports ===
import os
import logging
from datetime import datetime, timedelta

# === Third-Party Imports ===
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm
import mplfinance as mpf
from sqlalchemy import create_engine
from io import BytesIO
from dotenv import load_dotenv

# === Load Environment Variables ===
load_dotenv(dotenv_path='/mnt/c/Users/osamu/OneDrive/onedrive_python_source/envs/.env.uweb_11')  # <-- Immediately after importing it

# === Local Application Imports ===
from application.backend.stock_data_loader import download_stock_data

# Set up logging
logger = logging.getLogger(__name__)

# === Font Setup (Executed Once at Module Load) ===
FONT_PATH = os.path.join(os.path.dirname(__file__), 'fonts', 'NotoSansJP[wght].ttf')
FONT_PROP = fm.FontProperties(fname=FONT_PATH)

# Calculate the start and end dates based on the current date
end_date = datetime.now()
start_date = end_date - timedelta(days=10*365)  # Approximately 10 years before

# チャートの右端を見やすくするために新たに右端に余白を加えるためのend_date_plus_marginを計算 
end_date_plus_margin = end_date + timedelta(days=45)  # 45日分の余白を追加

def plot_combined_chart(seccode, engine):
    font_prop = FONT_PROP

    query = f'SELECT * FROM "d_fins_all_bps_opvalues" WHERE "seccode" = \'{seccode}\' ORDER BY "quarterenddate" ASC'

    df = pd.read_sql(query, engine)

    if df.empty:
        raise ValueError(f"No data found for Sec Code: {seccode}")

    df['quarterenddate'] = pd.to_datetime(df['quarterenddate'])
    df.sort_values(by='quarterenddate', inplace=True)

    companyname = df.iloc[-1]['companyname']

    fig, ax1 = plt.subplots(figsize=(18, 8))

    # Ensure that BPS and Operation Value stop at 0 even when negative
    bps_clipped = np.clip(df['bps'], 0, None)  # Clip the BPS values at 0
    bps_eval_clipped = np.clip(df['bps_eval'], 0, None)  # Clip the bps_eval values at 0
    opvalue_clipped = np.clip(df['bps_eval'] + df['opvalue'], 0, None)  # Clip the Operation Value at 0
    nextyrfcastfairvalue_clipped = np.clip(df['nextyrfcastfairvalue'], 0, None) # Clip forecasted fair value at 0

    # Fill between 0 and bps, and between bps and opvalue, stopping at 0 for negative values
    ax1.fill_between(df['quarterenddate'], 0, bps_eval_clipped, color='lightblue', alpha=0.3, step='mid', label='BPS')
    ax1.fill_between(df['quarterenddate'], bps_eval_clipped, opvalue_clipped, color='lightcoral', alpha=0.3, step='mid', label='Operation Value')
    # Fill area between bps_eval_clipped and bps_clipped
    ax1.fill_between(df['quarterenddate'], bps_eval_clipped, bps_clipped, color='lightcyan', alpha=0.4, step='mid', label='BPS Fill Area')

    # Prioritize the blue line (bps_eval Line) with the highest z-order
    ax1.step(df['quarterenddate'], bps_eval_clipped, color='blue', label='bps_eval Line', linestyle='--', where='mid', zorder=3)
    ax1.step(df['quarterenddate'], opvalue_clipped, color='orange', label='Fair Value Line', linestyle='-', where='mid', zorder=1)
    ax1.step(df['quarterenddate'], nextyrfcastfairvalue_clipped, label='Fair Value', color='gray', marker='x', where='mid', zorder=2)
    # New: Add bps_clipped line (highlight with distinct color and style)
    ax1.step(df['quarterenddate'], bps_clipped, label='BPS Clipped Line', color='cyan', linestyle='-.', where='mid', zorder=4)

    q4_data = df[df['quarter'] == 'FY']
    ax1.scatter(q4_data['quarterenddate'], q4_data['bps_eval'], color='blue', label='bps_eval (FY)', marker='*', s=100)
    ax1.scatter(q4_data['quarterenddate'], q4_data['bps_eval'] + q4_data['nextyrfcastopvalue'], color='red', label='Next Operation Value (FY)', marker='*', s=100)
    ax1.scatter(q4_data['quarterenddate'], q4_data['fairvalue'], color='green', label='Fair Value (FY)', marker='*', s=100)
    # 🔥 New: Add Scatter plot for key `bps_clipped` points
    ax1.scatter(df['quarterenddate'], bps_clipped, label='BPS Clipped (Points)', color='cyan', marker='*', s=40, zorder=5)

    # 配当率ラインの追加
    df['adjusted_divannual_for_chart'] = df['adjusted_divannual_for_chart'].fillna(0)
    dividend_yield_line = df['adjusted_divannual_for_chart'] / 0.04
    if not dividend_yield_line.empty:
        ax1.step(df['quarterenddate'], dividend_yield_line, label='Dividend Yield (4%)', color='purple', linestyle='-', where='mid')

    # 追加: FcastDivAnnual_for_chartの配当ラインをプロット
    df['adjusted_fcastdivannual_for_chart'] = df['adjusted_fcastdivannual_for_chart'].fillna(0)
    fcast_dividend_yield_line = df['adjusted_fcastdivannual_for_chart'] / 0.04
    if not fcast_dividend_yield_line.empty:
        ax1.step(df['quarterenddate'], fcast_dividend_yield_line, label='Forecast Dividend Yield (4%)', color='red', linestyle='--', where='mid')

    ax1.set_xlabel('Disclosed Date', fontproperties=font_prop)
    ax1.set_ylabel('Value', fontproperties=font_prop)
    ax1.set_title(f'Fair Values for Company {seccode} - {companyname}', fontproperties=font_prop)
    # ax1.grid(True)
    ax1.grid(True, axis='y')  # ✅ show horizontal price lines only
    ax1.legend(loc='upper left', prop=font_prop)

    ax1.yaxis.set_label_position("right")
    ax1.yaxis.tick_right()

    try:
        stock_data = download_stock_data(seccode)

    except Exception as e:
        logger.error(f"Failed to download or process stock data for {seccode} due to: {e}")
        img = BytesIO()
        plt.savefig(img, format='png', bbox_inches='tight', pad_inches=0.02)
        plt.close()
        img.seek(0)
        return img, companyname

    # mpf.plot(stock_data, type='candle', ax=ax1, style='charles', show_nontrading=True)
    mpf.plot(
        stock_data,
        type='ohlc',
        ax=ax1,
        style='charles',
        show_nontrading=True,
        update_width_config=dict(
            # candle_linewidth=0.5,
            # candle_width=5.0
            ohlc_linewidth=1.5,  # Make OHLC bars thicker
            ohlc_ticksize=3.0    # Extend open/close "ticks" wider
        )
    )

    #combined_dates = pd.date_range(start=min(df['quarterenddate'].min(), stock_data.index.min()), end=max(df['quarterenddate'].max(), stock_data.index.max()), freq='YS')
    # Use the same start_date and end_date for the x-axis limits
    ax1.set_xlim(start_date, end_date_plus_margin)

    # combined_dates = pd.date_range(start=start_date, end=end_date_plus_margin, freq='YS')   
    # combined_dates = pd.date_range(start=start_date, end=end_date_plus_margin, freq='6MS')  # Every 6 months
    combined_dates = pd.date_range(start=start_date, end=end_date_plus_margin, freq='2QS-JAN')

    for date in combined_dates:
        if date.month == 1:
            ax1.axvline(
                x=date,
                color='gray',
                linewidth=1.2,
                linestyle='-',   # solid line for January
                zorder=0
            )
        else:
            ax1.axvline(
                x=date,
                color='gray',
                linewidth=0.8,
                linestyle=(0, (4, 6)),  # dashed for July
                zorder=0
            )

    # Set the ticks (6-month grid lines: Jan + Jul)
    ax1.set_xticks(combined_dates)

    # Generate only the January label positions and text
    label_positions = [d for d in combined_dates if d.month == 1]
    label_texts = [d.strftime('%Y') for d in label_positions]

    # Set only the labeled ticks (once), with clean horizontal text
    ax1.set_xticks(label_positions)
    ax1.set_xticklabels(label_texts, fontproperties=font_prop, rotation=0)

    # 1. Calculate ymax
    ymax = max(
        df['bps'].max(),
        df['bps_eval'].max(),
        (df['bps_eval'] + df['opvalue']).max(),
        df['nextyrfcastfairvalue'].max(),
        df['adjusted_divannual_for_chart'].max() / 0.04,
        df['adjusted_fcastdivannual_for_chart'].max() / 0.04,
        df['fairvalue'].max(),
        stock_data['High'].max()
    )

    # 2. Set axis limits
    ax1.set_ylim(bottom=0, top=ymax * 1.1)

    # 3. Identify clipped series and collect names
    clipped_series = []
    if (df['bps'] < 0).any():
        clipped_series.append("bps")
    if (df['bps_eval'] < 0).any():
        clipped_series.append("bps_eval")
    if ((df['bps_eval'] + df['opvalue']) < 0).any():
        clipped_series.append("bps_eval + opvalue")
    if (df['nextyrfcastfairvalue'] < 0).any():
        clipped_series.append("nextyrfcastfairvalue")
    if (df['fairvalue'] < 0).any():
        clipped_series.append("fairvalue")
    if ((df['adjusted_divannual_for_chart'] / 0.04) < 0).any():
        clipped_series.append("dividend_yield")
    if ((df['adjusted_fcastdivannual_for_chart'] / 0.04) < 0).any():
        clipped_series.append("forecast_dividend_yield")

    # 4. Annotate if any value was clipped below zero
    # if clipped_series:
    if clipped_series:
        ax1.text(
            df['quarterenddate'].iloc[-1],
            ymax * 1.05,
            f"⚠️ CLIPPED: {', '.join(clipped_series)}",
            fontsize=12,
            color='red',
            ha='right',
            va='bottom'
        )

    plt.tight_layout()

    img = BytesIO()
    plt.savefig(img, format='png', bbox_inches='tight', pad_inches=0.02)
    plt.close()
    img.seek(0)

    return img, companyname

# テスト実行用
if __name__ == "__main__":

    load_dotenv(dotenv_path='/mnt/c/Users/osamu/OneDrive/onedrive_python_source/envs/.env.uweb_11')

    # Heroku環境かどうかを確認する
    heroku_env = os.getenv("HEROKU_ENV", "false").lower() == "true"
    if heroku_env:
        heroku_database_url = os.getenv('HEROKU_DATABASE_URL')
        heroku_database_url = heroku_database_url.replace('postgres://', 'postgresql+psycopg2://')
        engine = create_engine(heroku_database_url)
        print("Running in Heroku environment. Using Heroku database.")
    else:
        local_database_url = os.getenv('LOCAL_DATABASE_URL')
        local_database_url = local_database_url.replace('postgres://', 'postgresql+psycopg2://')
        engine = create_engine(local_database_url)
        print("Running in local environment. Using local database.")

    sec_code = "1515"  # テストするセキュリティコードを入力してください

    try:
        img, company_name = plot_combined_chart(sec_code, engine)
        plt.imshow(plt.imread(img))
        plt.axis('off')
        plt.show()
    except Exception as e:
        print(f"Failed to generate plot for Sec Code: {sec_code} due to {e}")


# uweb_12/plot_fins_all_netsales.py

import os
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm
from sqlalchemy import create_engine
from dotenv import load_dotenv
import matplotlib
from matplotlib.dates import DateFormatter, YearLocator
from io import BytesIO
from datetime import datetime, timedelta
import numpy as np

matplotlib.use('Agg')

# Calculate the start and end dates based on the current date
end_date = datetime.now()
start_date = end_date - timedelta(days=8*365)  # Approximately 10 years before

end_date_plus_margin = end_date + timedelta(days=45)  # 45日分の余白を追加

def plot_qonq_growth(seccode, engine):
    # Query for NetSales QonQ growth data and projected growth rate
    netsales_query = """
    SELECT "fiscalyearend", "quarter", "quarterenddate", "growth_percentage", "projected_growth_rate", "companyname"
    FROM "d_fins_all_netsales"
    WHERE "seccode" = %s
    ORDER BY "quarterenddate"
    """
    netsales_df = pd.read_sql(netsales_query, engine, params=(seccode,))

    if netsales_df.empty:
        raise ValueError(f"No NetSales growth data found for sec code: {seccode}")

    # Ensure the dates are in datetime format
    netsales_df['quarterenddate'] = pd.to_datetime(netsales_df['quarterenddate'])

    # Replace None or NaN in 'CompanyName' with a default value
    netsales_df['companyname'] = netsales_df['companyname'].fillna('Unknown Company')

    # Convert growth_percentage and projected_growth_rate to numeric, forcing any errors to NaN
    netsales_df['growth_percentage'] = pd.to_numeric(netsales_df['growth_percentage'], errors='coerce')
    netsales_df['projected_growth_rate'] = pd.to_numeric(netsales_df['projected_growth_rate'], errors='coerce')

    # Filter out rows only if both growth_percentage and projected_growth_rate are NaN
    netsales_df = netsales_df.dropna(subset=['growth_percentage', 'projected_growth_rate'], how='all')

    # Sort by the quarter end date
    netsales_df.sort_values(by='quarterenddate', inplace=True)

    # Get the company name for the title
    companyname = netsales_df['companyname'].iloc[0]

    # Construct the full path to the font file
    font_path = os.path.join(os.path.dirname(__file__), 'fonts', 'NotoSansJP[wght].ttf')
    font_prop = fm.FontProperties(fname=font_path)
    
    fig, ax1 = plt.subplots(figsize=(18, 4))

    # Plot NetSales QonQ growth percentage with green "x" markers as step plot
    if not netsales_df['growth_percentage'].isna().all():
        ax1.step(netsales_df['quarterenddate'], netsales_df['growth_percentage'], 
                 label='NetSales Growth (Q on Q)', color='orange', where='mid', marker='x', markerfacecolor='green', markeredgecolor='green')

    # Plot the entire projected growth rate as one line, using light blue "x" markers
    if not netsales_df['projected_growth_rate'].isna().all():
        ax1.step(netsales_df['quarterenddate'], netsales_df['projected_growth_rate'], 
                 label='Projected Growth Rate', color='blue', where='mid', linestyle='-', marker='x', markersize=4, markerfacecolor='lightblue', markeredgecolor='lightblue')

    # Initialize a flag to track whether the FY End label has been added to the legend
    label_added = False

   # Overlay large red stars specifically at FY end points
    for date, quarter, projected_rate in zip(netsales_df['quarterenddate'], netsales_df['quarter'], netsales_df['projected_growth_rate']):
        if quarter == "FY" and pd.notnull(projected_rate):
            if not label_added:
                ax1.scatter(date, projected_rate, color='red', marker='*', s=100, label='FY End')
                label_added = True  # Set the flag to True after adding the label
            else:
                ax1.scatter(date, projected_rate, color='red', marker='*', s=100)  # No label after the first point
            
            # Draw a vertical line at the fiscal year-end date
            ax1.axvline(date, color='black', linestyle=':', alpha=0.7)

    # Add the legend to the plot (only if at least one "FY End" marker was added)
    if label_added:
        ax1.legend()

    ax1.axhline(0, color='red', linestyle='--')

    ax1.set_xlabel('Date', fontproperties=font_prop)
    ax1.set_ylabel('Growth (%)', fontproperties=font_prop)
    ax1.set_title(f'Quarterly NetSales Growth (Q on Q) and Projected Growth Rate for {companyname} (Sec Code {seccode})', fontproperties=font_prop)

    ax1.yaxis.set_label_position("right")
    ax1.yaxis.tick_right()

    # Set the x-axis to the calculated start_date and end_date
    ax1.set_xlim(start_date, end_date_plus_margin)

    # X-axis formatting to show only the year
    ax1.xaxis.set_major_locator(YearLocator())  # Display major ticks at each year
    ax1.xaxis.set_major_formatter(DateFormatter('%Y'))  # Format the tick labels as year only
    plt.setp(ax1.get_xticklabels(), rotation=0, fontproperties=font_prop)

    # Add grid lines
    ax1.grid(True, which='both', linestyle='--', linewidth=0.5)

    # Add legend
    ax1.legend(loc='upper left', prop=font_prop)

    plt.tight_layout()

    img = BytesIO()
    plt.savefig(img, format='png', bbox_inches='tight', pad_inches=0.02)
    plt.close()
    img.seek(0)

    return img, companyname

# テスト実行用
if __name__ == "__main__":
    load_dotenv(dotenv_path='/mnt/c/Users/osamu/OneDrive/onedrive_python_source/envs/.env.uweb_11')
    database_url = os.getenv('LOCAL_DATABASE_URL').replace('postgres://', 'postgresql+psycopg2://')
    engine = create_engine(database_url)

    # 画像保存用のフォルダパスを設定
    output_folder = "output_images"
    # フォルダが存在しない場合は作成
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    img, companyname = plot_qonq_growth('1301', engine)
    # ファイルパスを指定
    file_path = os.path.join(output_folder, f'average_sales_growth_{companyname}.png')

    # ファイルを保存
    with open(file_path, 'wb') as f:
        f.write(img.getbuffer())

    print(f"Image saved to {file_path}")
