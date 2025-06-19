
# chart_viewer/utils/viewer_fetch.py

import os
import logging
import pandas as pd
import requests
import datetime as dt

# Setup logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s: %(message)s')

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

# def fetch_weekly_margin_interest(code, id_token, years: int = DEFAULT_YEARS):
#     headers = {'Authorization': f'Bearer {id_token}'}
#     from_date = dt.date.today() - dt.timedelta(days=365 * years)
#     url = f"https://api.jquants.com/v1/markets/weekly_margin_interest?code={code}&from={from_date.strftime('%Y-%m-%d')}"
#     r = requests.get(url, headers=headers)
#     df = pd.DataFrame(r.json().get("weekly_margin_interest", []))

#     if df.empty:
#         logging.warning("No margin interest data returned from API for code: %s", code)
#         return pd.DataFrame(columns=["Date", "Code", "ShortMarginTradeVolume", "LongMarginTradeVolume"])

#     df = df[["Date", "Code", "ShortMarginTradeVolume", "LongMarginTradeVolume"]]
#     df["ScaledShortMargin"] = df["ShortMarginTradeVolume"] / 1000
#     df["ScaledLongMargin"] = df["LongMarginTradeVolume"] / 1000
#     logging.info("Margin data retrieved from API:\n%s", df.tail())
#     return df

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

    shares_outstanding = fetch_shares_outstanding(code, id_token)
    if shares_outstanding:
        df["ShortMarginRatio"] = df["ShortMarginTradeVolume"] / shares_outstanding
        df["LongMarginRatio"] = df["LongMarginTradeVolume"] / shares_outstanding
        df["ShortMarginRatio (%)"] = (df["ShortMarginRatio"] * 100).round(2)
        df["LongMarginRatio (%)"] = (df["LongMarginRatio"] * 100).round(2)

        logging.info("📊 Margin data with ratios (last 5 rows):\n%s", df[[
            "Date", "ShortMarginTradeVolume", "LongMarginTradeVolume",
            "ShortMarginRatio (%)", "LongMarginRatio (%)"
        ]].tail())
    else:
        logging.warning("Missing shares_outstanding; skipping ratio calculation")

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
    url = f"https://api.jquants.com/v1/markets/short_selling_positions?code={code}&from={from_date.strftime('%Y-%m-%d')}"
    r = requests.get(url, headers=headers)
    df = pd.DataFrame(r.json().get("short_selling_positions", []))

    if df.empty:
        logging.warning("No short selling data returned from API for code: %s", code)
        return pd.DataFrame(columns=[
            "DisclosedDate", "CalculatedDate", "Code", "ShortSellerName",
            "InvestmentFundName", "ShortPositionsToSharesOutstandingRatio",
            "ShortPositionsInSharesNumber", "CalculationInPreviousReportingDate",
            "ShortPositionsInPreviousReportingRatio"
        ])

    df = df[[
        "DisclosedDate", "CalculatedDate", "Code", "ShortSellerName",
        "InvestmentFundName", "ShortPositionsToSharesOutstandingRatio",
        "ShortPositionsInSharesNumber", "CalculationInPreviousReportingDate",
        "ShortPositionsInPreviousReportingRatio"
    ]]

    df["CalculatedDate"] = pd.to_datetime(df["CalculatedDate"])
    df = df[df["CalculatedDate"].dt.date >= from_date]

    df["ShortPositionsRatio (%)"] = df["ShortPositionsToSharesOutstandingRatio"] * 100
    df["InferredTotalShares"] = df["ShortPositionsInSharesNumber"] / df["ShortPositionsToSharesOutstandingRatio"]

    shares_outstanding = fetch_shares_outstanding(code, id_token)
    df["ActualSharesOutstanding"] = shares_outstanding

    if shares_outstanding:
        df["InferredError (%)"] = abs(df["InferredTotalShares"] - shares_outstanding) / shares_outstanding * 100
    else:
        df["InferredError (%)"] = float("nan")
        logging.warning("Missing shares_outstanding, skipping InferredError calculation")

    logging.info("Short selling data with cross-check:\n%s", df[[
        "CalculatedDate", "ShortSellerName", "ShortPositionsInSharesNumber",
        "ShortPositionsRatio (%)", "InferredTotalShares",
        "ActualSharesOutstanding", "InferredError (%)"
    ]].tail())

    return df

def fetch_shares_outstanding(code, id_token):
    import requests
    import pandas as pd
    import logging

    url = f"https://api.jquants.com/v1/fins/statements?code={code}"
    headers = {'Authorization': f'Bearer {id_token}'}
    r = requests.get(url, headers=headers)

    if not r.ok:
        logging.error("Failed to fetch financial statements for %s: %s", code, r.text)
        return None

    data = r.json().get("statements", [])
    if not data:
        logging.warning("No statement data returned for code %s", code)
        return None

    df = pd.DataFrame(data)
    df["DisclosedDate"] = pd.to_datetime(df["DisclosedDate"], errors="coerce")
    df = df[df["TypeOfDocument"].str.contains("FinancialStatements", na=False)]
    df = df.sort_values("DisclosedDate", ascending=False)

    # Candidate columns in order of preference
    candidates = [
        "NumberOfIssuedAndOutstandingSharesAtTheEndOfFiscalYearIncludingTreasuryStock",
        "NumberOfIssuedAndOutstandingSharesAtTheEndOfFiscalYear"
    ]

    for col in candidates:
        if col in df.columns and df[col].notna().any():
            value = df[df[col].notna()].iloc[0][col]
            doc_type = df[df[col].notna()].iloc[0]["TypeOfDocument"]
            logging.info("Using '%s' from TypeOfDocument='%s'", col, doc_type)
            try:
                clean = str(value).replace(",", "").strip()
                if not clean or clean.lower() == "nan":
                    raise ValueError("Invalid value")
                return int(float(clean))
            except Exception as e:
                logging.error("Parsing error for shares outstanding: %s", e)
                return None

    logging.warning("No shares outstanding field found in latest FinancialStatements for code %s", code)
    return None

