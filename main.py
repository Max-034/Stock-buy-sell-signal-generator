import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

n50 = pd.read_csv('ns.csv')

# removing empty rows from the data
n50 = n50.dropna()

# calculating % change in the closing price of the stock ( daily return ).
n50.loc[: , 'Daily Returns'] = n50['Close'].pct_change()

# calculating volatility by calculating the standard deviation in the daily return values over a period of 15 days.
n50.loc[: , 'Volatility'] = n50['Daily Returns'].rolling(window=15).std()

# calculating the logarithm returns , using the shift function to use the closing value of previous day ( previous column).
n50.loc[: , 'Log Returns'] = np.log(n50['Close'] / n50['Close'].shift(1))

# calculating Simple Moving Average over 50 days window.( using the mean function)
n50.loc[: , 'SMA 50'] = n50['Close'].rolling(window= 50).mean()

#calculating Simple Moving Average over 200 days window. ( using mean function )
n50.loc[: , 'SMA 200'] = n50['Close'].rolling(window= 200).mean()

# making a new column Signal , which will have the value 1 if the condition for generating the buy signal is satisfied and will have value 0 if the condition for generating sell signal is satisfied , otherwise it will have NaN value.
n50.loc[(n50['SMA 50'] > n50['SMA 200']) & (n50['SMA 50'].shift(1) <= n50['SMA 200'].shift(1)), 'Signal'] = 1
n50.loc[(n50['SMA 50'] < n50['SMA 200']) & (n50['SMA 50'].shift(1) >= n50['SMA 200'].shift(1)) , 'Signal'] = 0



pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
plt.figure(figsize=(16,8))
plt.plot(n50['Date'], n50[['Close', 'SMA 200', 'SMA 50']])


# Adding labels for x and y axes
plt.xlabel('Date')
plt.ylabel('Value')
# Adding a legend
plt.legend(['Close', 'SMA 200', 'SMA 50'])
# Showing the plot

buy_signals = n50[n50['Signal'] == 1]
sell_signals = n50[n50['Signal'] == 0]

# putting markers in the graph for buy and sell signals
plt.scatter(buy_signals['Date'], buy_signals['SMA 200'], color='green', marker='^', label='Buy Signal')
plt.scatter(sell_signals['Date'], sell_signals['SMA 200'], color='red', marker='v', label='Sell Signal')

# Adding labels for x and y axes
x_ticks_positions = n50.index[::200]  # Take every 100th index value
plt.xticks(x_ticks_positions)
plt.show()


# initialising invested capital ( assuming to be 10000000) , portfolio value , stocks owned and a list of returns for each trade.
capital = 10000000
portfolio = 0
stocks = 0
returns = []
buyprice = 0
# iterating over every row ( every day) in dataframe and keeping track of capital , portfolio ,buy price ,  stocks and returns.

for date, signal in n50['Signal'].iteritems():

  #updating portfolio as per the closing price of each day.
  portfolio = float(n50.at[date , 'Close'])*stocks + capital

  #tracking portfolio value everyday
  n50.at[date , 'Portfolio Value'] = portfolio
  #tracking peak portfolio value everyday(for calculating maxdrawdown)
  n50.at[date , 'Peak Value'] = n50['Portfolio Value'].max()
  #tracking % drawdown everyday
  n50.at[date , '% drawdown'] = ((n50.at[date , 'Peak Value'] - portfolio) / n50.at[date , 'Peak Value']) * 100

  if signal ==  1 and portfolio == capital:
    stocks = int(capital/n50.at[date , 'Close'])
    capital = capital - float(n50.at[date , 'Close'])*stocks
    portfolio = float(n50.at[date , 'Close'])*stocks + capital
    buyprice = float(n50.at[date , 'Close'])

  elif signal == 0 and portfolio > capital:
    k = portfolio - buyprice*float(stocks)
    returns.append(k)
    capital = capital + float(n50.at[date , 'Close'])*stocks
    returns.append(capital)
    stocks = 0
    portfolio = capital



#calculating maximum drawdown
maxdrawdown = n50['% drawdown'].max()



#calculating trading years , based on the fact that there are 252 trading days in one year.
years = len(n50) / 252
#calculating annual return
annualreturn = (capital/10000000)**(1/years) - 1

#plotting equity curve
plt.figure(figsize=(16,8))
plt.plot(n50['Date'], n50['Portfolio Value'])
plt.xlabel('Date')
plt.ylabel('Trading Account Value')
x_ticks_positions = n50.index[::200]  # Take every 100th index value
plt.xticks(x_ticks_positions)
plt.show()



print("Trading Capital: " + str(capital) + "\n")
print("List of Returns: ")
print(returns)
print("Annual Returns: " + str(annualreturn) + "\n")
print("Maximum Drawdown: " + str(maxdrawdown))

















