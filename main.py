import requests
import pandas as pd
import streamlit as st
import plotly.express as px
from groq import Groq
import os
from streamlit_plotly_events import plotly_events

base_url = 'https://financialmodelingprep.com/api'
API_KEY = 'ec2letPFIDhtcs86wM4eQcZ4WAXLuB7y'
GROQ = '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'  # Replace with your actual OpenAI API key

st.set_page_config(layout="wide")
st.title('AI-Powered Financial Insight')

ticker = st.sidebar.text_input('Ticker:', value='AAPL')

client = Groq(api_key=GROQ)

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
    fig = px.bar(x=x, y=y, title=title)  # Changed from px.line to px.bar
    fig.update_layout(xaxis_title='Year', yaxis_title=y_axis_title)
    return fig

def get_ai_insight(data, selected_range, metric):
    prompt = f"Analyze the {metric} data for {ticker} from {selected_range[0]} to {selected_range[1]}. The data is {data}. Provide insights on significant trends, potential causes, and implications for the company's financial health. Consider macroeconomic factors and industry-specific news that might have influenced these changes."
    
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a financial analyst providing insights on company performance."},
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

# Create and display graphs with AI insights
st.header(f"Financial Metrics for {ticker}")

col1, col2 = st.columns(2)

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

for i, (metric_name, metric_data) in enumerate(metrics):
    with col1 if i % 2 == 0 else col2:
        fig = create_plot(years, metric_data, f'{metric_name} Over Time', metric_name)
        selected_points = plotly_events(fig, click_event=False, select_event=True)
        
        if selected_points:
            selected_range = [min(point['x'] for point in selected_points),
                              max(point['x'] for point in selected_points)]
            selected_data = [d for y, d in zip(years, metric_data) if selected_range[0] <= y <= selected_range[1]]
            
            insight = get_ai_insight(selected_data, selected_range, metric_name)
            st.write(f"AI Insight for {metric_name} ({selected_range[0]} - {selected_range[1]}):")
            st.write(insight)
