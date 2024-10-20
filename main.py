import requests
import pandas as pd
import streamlit as st
import plotly.express as px
from groq import Groq
import os
from streamlit_plotly_events import plotly_events
import plotly.graph_objects as go

# Configuration
base_url = 'https://financialmodelingprep.com/api'
API_KEY = 'xu2Xh5xcSrglcMecHrV30YOgf71pnFpg'
GROQ = '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'  # Replace with your actual GROQ API key

st.set_page_config(layout="wide")
st.title('AI-Powered Financial Insight')

# Sidebar for user input
ticker = st.sidebar.text_input('Ticker:', value='AAPL')

# Initialize Groq client
client = Groq(api_key=GROQ)

# Function definitions
def get_financial_data(statement_type):
    url = f'{base_url}/v3/{statement_type}/{ticker}?period=annual&limit=5&apikey={API_KEY}'
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raises an HTTPError for bad responses
        data = response.json()

        if isinstance(data, str):
            st.error(f"Error in {statement_type} data: {data}")
            return []
        elif isinstance(data, list) and len(data) > 0:
            return data
        else:
            st.error(f"Invalid data format for {statement_type}")
            return []
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching {statement_type} data: {e}")
        return []
    except ValueError as e:
        st.error(f"Error parsing JSON for {statement_type}: {e}")
        return []

def create_plot(x, y, title, y_axis_title):
    fig = px.bar(x=x, y=y, title=title)
    fig.update_layout(xaxis_title='Year', yaxis_title=y_axis_title)
    return fig
def get_ai_insight(ticker, data, year_range, metric):
    if len(year_range) == 1:
        prompt = f"Analyze the {metric} data point for {ticker} in {year_range[0]}. The value is {data[0]}. Provide insights on this specific data point, its significance, and how it compares to industry standards or the company's historical performance. Most importantly, you are to only utilize specific company performance data from the dataset that we have provided from financialmodelingprep.com. Consider any relevant macroeconomic factors or company specific factors from this period that might explain this value. Make the information as concise as possible. Most importantly, you are to only utilize specific company performance data from the dataset that we have provided from financialmodelingprep.com."
    else:
        prompt = f"Analyze the {metric} data for {ticker} from {year_range[0]} to {year_range[1]}. The data is {data}. Provide insights on this specific data point, its significance, and how it compares to industry standards or the company's historical performance. Most importantly, you are to only utilize specific company performance data from the dataset that we have provided from financialmodelingprep.com. Consider any relevant macroeconomic factors or company specific factors from this period that might explain this value. Make the information as concise as possible. Most importantly, you are to only utilize specific company performance data from the dataset that we have provided from financialmodelingprep.com."
    
    response = client.chat.completions.create(
        model="mixtral-8x7b-32768",
        messages=[
            {"role": "system", "content": "Provide insights on this specific data point, its significance, and how it compares to industry standards or the company's historical performance. Most importantly, you are to only utilize specific company performance data from the dataset that we have provided from financialmodelingprep.com. Consider any relevant macroeconomic factors or company specific factors from this period that might explain this value. Make the information as concise as possible. Most importantly, you are to only utilize specific company performance data from the dataset that we have provided from financialmodelingprep.com."},
            {"role": "user", "content": prompt}
        ]
    )

    return response.choices[0].message.content

# Fetch data
income_data = get_financial_data('income-statement')
balance_sheet_data = get_financial_data('balance-sheet-statement')
cash_flow_data = get_financial_data('cash-flow-statement')

# Process data
if income_data and balance_sheet_data and cash_flow_data:
    try:
        years = [data['date'][:4] for data in income_data]
        revenue = [data['revenue'] for data in income_data]
        eps = [data['eps'] for data in income_data]
        gross_profit_ratio = [data['grossProfitRatio'] for data in income_data] 
        net_income_ratio = [data['netIncomeRatio'] for data in income_data] 
        net_income = [data['netIncome'] for data in income_data]
        total_assets = [data['totalAssets'] for data in balance_sheet_data]
        total_liabilities = [data['totalLiabilities'] for data in balance_sheet_data]
        operating_cash_flow = [data['operatingCashFlow'] for data in cash_flow_data]
        free_cash_flow = [data['freeCashFlow'] for data in cash_flow_data]
        total_current_assets = [data['totalCurrentAssets'] for data in balance_sheet_data] 
        total_current_liabilities = [data['totalCurrentLiabilities'] for data in balance_sheet_data]
        liquidity = [int(a)/int(b) for a,b in zip(total_current_assets, total_current_liabilities)]
    except (KeyError, TypeError) as e:
        st.error(f"Error processing financial data: {e}")
        st.error("Please check the API response format and ensure all required fields are present.")
        years, revenue, eps, gross_profit_ratio, net_income_ratio, net_income, total_assets, total_liabilities, operating_cash_flow, free_cash_flow, total_current_assets, total_current_liabilities, liquidity = ([] for _ in range(13))
else:
    st.error("Some or all financial data is missing. Please check the API response.")
    years, revenue, eps, gross_profit_ratio, net_income_ratio, net_income, total_assets, total_liabilities, operating_cash_flow, free_cash_flow, total_current_assets, total_current_liabilities, liquidity = ([] for _ in range(13))

# Define metrics
metrics = [
    ('Revenue', revenue),
    ('EPS', eps),
    ('Gross Profit Ratio', gross_profit_ratio),
    ('Net Income', net_income),
    ('Net Income Ratio', net_income_ratio),
    ('Total Liabilities', total_liabilities),
    ('Total Assets', total_assets),
    ('Free Cash Flow', free_cash_flow),
    ('Current Ratio', liquidity),
    ('Operating Cash Flow', operating_cash_flow)
]

# Create and display graphs with AI insights
st.header(f"Financial Metrics for {ticker}")

col1, col2 = st.columns(2)

def display_styled_insight(insight):
    styled_insight = f"""
    <div style="font-family: SF Pro, sans-serif; font-size: 15px;">
    {insight}
    </div>
    """
    st.markdown(styled_insight, unsafe_allow_html=True)

for i, (metric_name, metric_data) in enumerate(metrics):
    with col1 if i % 2 == 0 else col2:
        fig = create_plot(years, metric_data, f'{metric_name} Over Time', metric_name)
        hovered_points = plotly_events(fig, click_event=False, hover_event=True)
        
        if hovered_points:
            hovered_year = hovered_points[0]['x']
            hovered_value = hovered_points[0]['y']
            
            insight = get_ai_insight(ticker, [hovered_value], [hovered_year], metric_name)
            display_styled_insight(f"AI Analyst Insight for {metric_name} ({hovered_year}):")
            display_styled_insight(insight)