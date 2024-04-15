## DESCRIPTION: This program visualizes my stock portfolio

# Importing the libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import random

# Load the data
df = pd.read_csv('portfolio.csv')

# Get the total invested amount of money in the portfolio
Portfolio_Total_Amount = sum(df['Amount'] * df['Average_Price'])
Portfolio_Total_Amount = round(Portfolio_Total_Amount, 2)

# Visually show the portfolio and some additional information
stock_tickers = df['Tickers'].values
sizes = df['Amount'] * df['Average_Price']

listOfZeros = [0] * df.shape[0]
n = random.randint(0, df.shape[0]-1)
listOfZeros[n] = 0.1
explode = listOfZeros

#### Create a figure
fig1, ax1 = plt.subplots(figsize=(10,10))

# Plot the pie chart
ax1.pie(sizes, explode=explode, labels=stock_tickers, autopct = '%.2f%%', shadow='True', startangle=360)

# Set the title
ax1.set_title('Portfolio Pie Chart', color='Purple', fontsize=22)

# Add text to the visual
x = -1.75
y = 1
ax1.text(x, y, 'Overview:', fontsize=24, color='Purple')

y_counter = 0.12
ax1.text(x, y - y_counter, 'Total: $'+str(Portfolio_Total_Amount), fontsize=15, color='Blue')

for i in range(0, df.shape[0]):
    ax1.text(x, 0.88 - y_counter, df['Tickers'][i]+ ': $' + str(round(df['Amount'][i]*df['Average_Price'][i],2)), fontsize=14, color='Black')
    y_counter = y_counter + 0.12
plt.show()

