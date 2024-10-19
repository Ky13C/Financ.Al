import requests
import pandas as pd 
import streamlit as st 


base_url = 'https://financialmodelingprep.com/api'
API_KEY = 'gueI3DrDFSZOHCrY67gVrL1QbaWXciFf'

st.header('Financial Analysis Model')
ticker = st.sidebar.text_input('Ticker:', value = 'AAPL')
financial_data = st.sidebar.selectbox('Financial Data Type', options = ('income-statement', 'balance-sheet-statement',
                                                                        'cash-flow-statement', 'income-statement-growth',
                                                                        'balance-sheet-statement-growth', 'cash-flow-statement-growth'))


url = f'{base_url}/v3/{financial_data}/{ticker}?period=annual&apikey={API_KEY}'
response = requests.get(url)
data = response.json()

df = pd.DataFrame(data).T
st.write(df)