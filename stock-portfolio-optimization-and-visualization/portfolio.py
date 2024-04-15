## Description: This program attempts to optimize a users portfolio using the Efficient Frontier

# import the python libraries
import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
from pypfopt.efficient_frontier import EfficientFrontier
from pypfopt import risk_models
from pypfopt import expected_returns

plt.style.use('fivethirtyeight')

# Get the stocks symbols/tickers in the portfolio
# FAANG
assets = ['META', 'AMZN', 'NFLX', 'AAPL', 'GOOG']

# Assign weights to the stocks
weights = np.array([0.2,0.2,0.2,0.2,0.2])

# Get the stock/portfolio starting date
stockStartDate = '2013-01-01'

# Get the stocks ending date
stockEndDate = datetime.today().strftime('%Y-%m-%d')

# Create a dataframe to store the adjusted close price of the stocks
df = pd.DataFrame()

# Store the adjusted close price of the stock into the df
for stock in assets:
    df[stock] = yf.download(stock, start=stockStartDate, end=stockEndDate)['Adj Close']
    
# Visually show the stock / portfolio
title = 'Portfolio Adj. Close Price History'

# Get the stocks
my_stocks = df

# Create and plot the graph
for c in my_stocks.columns.values:
    plt.plot(my_stocks[c], label=c)
    
plt.title(title)
plt.xlabel('Date', fontsize=18)
plt.ylabel('Adj. Close USD ($)', fontsize=18)
plt.legend(my_stocks.columns.values, loc='upper left')
plt.show()

# Show the daily simple return
returns = df.pct_change()

# Create and show the annualized covariance matrix
cov_matrix_annual = returns.cov() * 252

# Calculate the portfoli ovariance
port_variance = np.dot(weights.T, np.dot(cov_matrix_annual, weights))
port_variance

# Calculate the portfolio volatility aka standard deviation
port_volatility = np.sqrt(port_variance)
port_volatility

# Calculate the annual portfolio return 
portfolioSimpleAnnualReturn = np.sum(returns.mean() * weights) * 252

# Show the expected annual return, volatility (risk) and variance
percent_var = str(round(port_variance, 2)*100) + '%'
percent_vols = str(round(port_volatility, 2)*100)+'%'
percent_ret = str(round(portfolioSimpleAnnualReturn,2)*100) + '%'

print('Expected annural return: ' + percent_ret)
print('annual_volatility /risk: ' + percent_vols)
print('Annual variance: ' + percent_var)

# Portfolio Optimization!
# Calculate the expected returns and the annualized sample covariance matrix of asset returns
mu = expected_returns.mean_historical_return(df)
S = risk_models.sample_cov(prices=df)

# optimize for max sharpe ratio
ef = EfficientFrontier(expected_returns=mu, cov_matrix=S)
weights = ef.max_sharpe()
cleaned_weights = ef.clean_weights()
print(cleaned_weights)
ef.portfolio_performance(verbose=True)

# 0.13632 + 0.16717 + 0.30602 + 0.3579 + 0.03259 == 1.0

# Get the discrete allocation of each share per stock
from pypfopt.discrete_allocation import DiscreteAllocation, get_latest_prices

latest_prices = get_latest_prices(df)
weights = cleaned_weights
da = DiscreteAllocation(weights, latest_prices, total_portfolio_value=15000)
allocation, leftover = da.lp_portfolio()
print('Discrete Allocation:', allocation)
print('Funds remaining: ${:.2f}'.format(leftover))

# save the data into a csv file
portfolio_df = pd.DataFrame({'Tickers': latest_prices.index, 'Average_Price': np.round(latest_prices.values,2)})

portfolio_df['Amount'] = list(allocation.values())

portfolio_df.to_csv('portfolio.csv', header=True, index=False)


