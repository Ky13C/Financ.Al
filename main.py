import requests
import pandas as pd
import streamlit as st
import plotly.graph_objs as go

base_url = 'https://financialmodelingprep.com/api'
API_KEY = 'gueI3DrDFSZOHCrY67gVrL1QbaWXciFf'

st.set_page_config(layout="wide")
st.title('Financial Analysis Model')

ticker = st.sidebar.text_input('Ticker:', value='AAPL')

def get_financial_data(statement_type):
    url = f'{base_url}/v3/{statement_type}/{ticker}?period=annual&limit=5&apikey={API_KEY}'
    response = requests.get(url)
    return response.json()

def create_plot(x, y, title, y_axis_title):
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x, y=y, mode='lines+markers'))
    fig.update_layout(title=title, xaxis_title='Year', yaxis_title=y_axis_title)
    return fig

# Fetch data
income_data = get_financial_data('income-statement')
balance_sheet_data = get_financial_data('balance-sheet-statement')
cash_flow_data = get_financial_data('cash-flow-statement')

# Process data
years = [data['date'][:4] for data in income_data]
revenue = [data['revenue'] for data in income_data]
net_income = [data['netIncome'] for data in income_data]
total_assets = [data['totalAssets'] for data in balance_sheet_data]
total_liabilities = [data['totalLiabilities'] for data in balance_sheet_data]
operating_cash_flow = [data['operatingCashFlow'] for data in cash_flow_data]
free_cash_flow = [data['freeCashFlow'] for data in cash_flow_data]
# Create and display graphs
st.header(f"Financial Metrics for {ticker}")

col1, col2 = st.columns(2)

with col1:
    st.plotly_chart(create_plot(years, revenue, 'Revenue Over Time', 'Revenue ($)'), use_container_width=True)
    st.plotly_chart(create_plot(years, total_assets, 'Total Assets Over Time', 'Total Assets ($)'), use_container_width=True)
    st.plotly_chart(create_plot(years, operating_cash_flow, 'Operating Cash Flow Over Time', 'Operating Cash Flow ($)'), use_container_width=True)

with col2:
    st.plotly_chart(create_plot(years, net_income, 'Net Income Over Time', 'Net Income ($)'), use_container_width=True)
    st.plotly_chart(create_plot(years, total_liabilities, 'Total Liabilities Over Time', 'Total Liabilities ($)'), use_container_width=True)
    st.plotly_chart(create_plot(years, free_cash_flow, 'Free Cash Flow Over Time', 'Free Cash Flow ($)'), use_container_width=True)
