"""
Impelementation of Modern Portolio Theory
"""

import numpy as np
import pandas as pd
import yfinance as yf
import datetime as dt

# Import data
def getData(stocks, start, end):
    stockData = yf.download(stocks, start, end)
    stockData = stockData['Close']
    
    returns = stockData.pct_change()
    meanReturns = returns.mean()
    covMatrix = returns.cov()

    return meanReturns, covMatrix

def portfolio_performance(weights, meanReturns, covMatrix):
    returns = np.sum(meanReturns*weights)*252
    std = np.sqrt(np.dot(weights.T, np.dot(covMatrix, weights))) * np.sqrt(252)
    return returns, std

stockList = ['CBA', 'BHP', "TLS"]
stocks = [stock+'.AX' for stock in stockList]

endDate = dt.datetime.now()
startDate = endDate - dt.timedelta(days=365)

weights = np.array([0.3, 0.3, 0.4])

meanReturns , covMatrix = getData(stocks, startDate, endDate)

returns, std = portfolio_performance(weights, meanReturns, covMatrix)
print(round(returns*100, 2), round(std*100, 2))