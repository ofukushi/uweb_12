
# application/backend/viewer_utils/chart_plotly.py

import pandas as pd
import plotly.graph_objs as go

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
        return None  # ✅ clean return
    return go.Scatter(
        x=df_shorts["CalculatedDate"],
        y=df_shorts["ScaledShortShares"],
        mode='lines+markers',
        name="Outstanding Short Positions",
        yaxis="y2",
        line=dict(color='darkorange', width=2, dash='dot')
    )

def create_combined_chart(df_prices, df_margin, df_shorts, company_name, seccode=None):
    df_prices['Date'] = pd.to_datetime(df_prices['Date'])
    df_margin['Date'] = pd.to_datetime(df_margin['Date'])

    df_margin['ScaledShortMargin'] = df_margin['ShortMarginTradeVolume'] / 1000
    df_margin['ScaledLongMargin'] = df_margin['LongMarginTradeVolume'] / 1000

    traces = [
        plot_candlestick(df_prices),
        plot_long_margin(df_margin),
        plot_short_margin(df_margin)
    ]

    if df_shorts is not None and not df_shorts.empty and 'CalculatedDate' in df_shorts.columns:
        df_shorts['CalculatedDate'] = pd.to_datetime(df_shorts['CalculatedDate'])
        trace = plot_short_selling_positions(df_shorts)
        if trace:
            traces.append(trace)

    max_margin = max(df_margin["ScaledShortMargin"].max(), df_margin["ScaledLongMargin"].max())
    y2_range = [0, max_margin * 1.2]

    # Strip trailing "0" if seccode ends with it
    display_code = seccode[:-1] if seccode and seccode.endswith("0") else seccode
    title_prefix = f"{company_name} ({display_code})" if display_code else company_name or "Stock"
    
    fig = go.Figure(data=traces)
    fig.update_layout(
        title=f'{title_prefix} - Stock Price & Margin Interest',
        xaxis=dict(title='Date'),
        yaxis=dict(title='Price'),
        yaxis2=dict(
            title='Margin / Short Vol. (×1,000)',
            overlaying='y',
            side='right',
            showgrid=False,
            showticklabels=True,
            range=y2_range,
        ),
        height=750,
        autosize=True,
        barmode='overlay'
    )

    return fig.to_html(full_html=False)
