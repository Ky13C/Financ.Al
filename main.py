import matplotlib.pyplot as plt
import numpy as np

# Sample data
quarters = ['Q4 2020', 'Q2 2021', 'Q4 2021', 'Q2 2022', 'Q4 2022', 'Q2 2023', 'Q4 2023', 'Q2 2024']
price = np.random.uniform(160, 240, len(quarters))
revenue = np.random.uniform(80, 130, len(quarters))
ebitda = np.random.uniform(20, 40, len(quarters))
free_cash_flow = np.random.uniform(15, 45, len(quarters))
net_income = np.random.uniform(10, 35, len(quarters))
eps = np.random.uniform(0.5, 2.5, len(quarters))
cash = np.random.uniform(40, 100, len(quarters))
debt = np.random.uniform(60, 120, len(quarters))
dividends = np.random.uniform(0.15, 0.25, len(quarters))
shares_outstanding = np.full(len(quarters), 16)
ratios = np.random.uniform(8, 18, len(quarters))
valuation = np.random.uniform(15, 40, len(quarters))

# Create subplots
fig, axes = plt.subplots(nrows=4, ncols=3, figsize=(15, 10))
fig.tight_layout(pad=5.0)

# Price graph
axes[0, 0].plot(price)
axes[0, 0].set_title('Price')
axes[0, 0].set_xticklabels(quarters)

# Revenue graph
axes[0, 1].bar(quarters, revenue)
axes[0, 1].set_title('Revenue')

# EBITDA graph
axes[1, 0].bar(quarters, ebitda)
axes[1, 0].set_title('EBITDA')

# Free Cash Flow graph
axes[1, 1].bar(quarters, free_cash_flow)
axes[1, 1].set_title('Free Cash Flow')

# Net Income graph
axes[1, 2].bar(quarters, net_income)
axes[1, 2].set_title('Net Income')

# EPS graph
axes[2, 0].bar(quarters, eps)
axes[2, 0].set_title('EPS')

# Cash & Debt graph
axes[2, 1].bar(quarters, cash)
axes[2, 1].bar(quarters, debt)
axes[2, 1].set_title('Cash & Debt')

# Dividends graph
axes[2, 2].bar(quarters, dividends)
axes[2, 2].set_title('Dividends')

# Shares Outstanding graph
axes[3, 0].bar(quarters, shares_outstanding)
axes[3, 0].set_title('Shares Outstanding')

# Ratios graph
axes[3, 1].bar(quarters, ratios)
axes[3, 1].set_title('Ratios')

# Valuation graph
axes[3, 2].plot(valuation)
axes[3, 2].set_title('Valuation')

plt.show()