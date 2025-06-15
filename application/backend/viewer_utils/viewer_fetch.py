
# chart_viewer/utils/margin.py

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
