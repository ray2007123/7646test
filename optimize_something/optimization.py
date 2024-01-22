""""""
"""MC1-P2: Optimize a portfolio.  		  	   		 	   			  		 			     			  	 
  		  	   		 	   			  		 			     			  	 
Copyright 2018, Georgia Institute of Technology (Georgia Tech)  		  	   		 	   			  		 			     			  	 
Atlanta, Georgia 30332  		  	   		 	   			  		 			     			  	 
All Rights Reserved  		  	   		 	   			  		 			     			  	 
  		  	   		 	   			  		 			     			  	 
Template code for CS 4646/7646  		  	   		 	   			  		 			     			  	 
  		  	   		 	   			  		 			     			  	 
Georgia Tech asserts copyright ownership of this template and all derivative  		  	   		 	   			  		 			     			  	 
works, including solutions to the projects assigned in this course. Students  		  	   		 	   			  		 			     			  	 
and other users of this template code are advised not to share it with others  		  	   		 	   			  		 			     			  	 
or to make it available on publicly viewable websites including repositories  		  	   		 	   			  		 			     			  	 
such as github and gitlab.  This copyright statement should not be removed  		  	   		 	   			  		 			     			  	 
or edited.  		  	   		 	   			  		 			     			  	 
  		  	   		 	   			  		 			     			  	 
We do grant permission to share solutions privately with non-students such  		  	   		 	   			  		 			     			  	 
as potential employers. However, sharing with other current or future  		  	   		 	   			  		 			     			  	 
students of CS 7646 is prohibited and subject to being investigated as a  		  	   		 	   			  		 			     			  	 
GT honor code violation.  		  	   		 	   			  		 			     			  	 
  		  	   		 	   			  		 			     			  	 
-----do not edit anything above this line---  		  	   		 	   			  		 			     			  	 
  		  	   		 	   			  		 			     			  	 
Student Name: Tucker Balch (replace with your name)  		  	   		 	   			  		 			     			  	 
GT User ID: mwang611 (replace with your User ID)  		  	   		 	   			  		 			     			  	 
GT ID: 903561880 (replace with your GT ID)  		  	   		 	   			  		 			     			  	 
"""

import datetime as dt
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import scipy.optimize as spo
from util import get_data, plot_data


def optimize_portfolio(
        sd=dt.datetime(2008, 1, 1),
        ed=dt.datetime(2009, 1, 1),
        syms=["GOOG", "AAPL", "GLD", "XOM"],
        gen_plot=False,
):
    # Read in adjusted closing prices for given symbols, date range
    dates = pd.date_range(sd, ed)
    prices_all = get_data(syms, dates)  # automatically adds SPY
    prices = prices_all[syms]  # only portfolio symbols
    prices_SPY = prices_all["SPY"]  # only SPY, for comparison later

    # find the allocations for the optimal portfolio
    allocs = find_optimal_allocations(prices)

    # Calculate portfolio statistics
    cr, adr, sddr, sr = calculate_portfolio_statistics(prices, allocs)

    # Get daily portfolio value
    port_val = calculate_daily_portfolio_value(prices, allocs)

    # Compare daily portfolio value with SPY using a normalized plot
    if gen_plot:
        plot_normalized_portfolio(port_val, prices_SPY)

    return allocs, cr, adr, sddr, sr

def find_optimal_allocations(prices):
    # Initial guess: Equal allocation
    allocs = np.ones(prices.shape[1]) / prices.shape[1]

    # Define bounds for each stock allocation (0 to 1)
    bounds = [(0.0, 1.0)] * prices.shape[1]

    # Define equality constraint (sum of allocations = 1)
    constraint = {'type': 'eq', 'fun': lambda x: np.sum(x) - 1}

    # Minimize negative Sharpe ratio to maximize Sharpe ratio
    min_result = spo.minimize(
        negative_sharpe_ratio, allocs, method='SLSQP', args=(prices,), bounds=bounds, constraints=[constraint],
        options={'disp': True, 'maxiter': 1000}
    )

    return min_result.x

def negative_sharpe_ratio(allocs, prices):
    portfolio_values = get_portfolio(prices, allocs, 1)
    daily_returns = cal_daily_returns(portfolio_values)
    sharpe_ratio = opt_sharpe_ratio(daily_returns)
    return -sharpe_ratio

def get_portfolio(prices, alloc, initial_amount):
    # Normalize values
    T_prices = prices / prices.iloc[0]
    T_prices = T_prices * alloc
    T_prices = T_prices * initial_amount
    # daily_total_value ---->  portfolio
    portfolio_V = T_prices.sum(axis=1)
    return portfolio_V

def cal_daily_returns(portfolio_values):
    daily_returns = portfolio_values.copy()
    daily_returns[1:] = portfolio_values[1:] / portfolio_values[:-1].values - 1
    daily_returns = daily_returns[1:]
    return daily_returns

def cal_avg_daily_returns(daily_returns):
    return daily_returns.mean()

def cal_std_daily_returns(daily_returns):
    return daily_returns.std()

def sum_cummulative_returns(portfolio_values):
    return (portfolio_values[-1] / portfolio_values[0]) - 1

def opt_sharpe_ratio(daily_returns):
    return np.sqrt(252) * cal_avg_daily_returns(daily_returns) / cal_std_daily_returns(daily_returns)

def calculate_portfolio_statistics(prices, allocs):
    cr = calculate_cumulative_return(prices, allocs)
    adr = calculate_average_daily_return(prices, allocs)
    sddr = calculate_standard_deviation_of_daily_returns(prices, allocs)
    sr = calculate_sharpe_ratio(prices, allocs)
    return cr, adr, sddr, sr

def calculate_cumulative_return(prices, allocs):
    port_val = calculate_daily_portfolio_value(prices, allocs)
    return (port_val[-1] / port_val[0]) - 1

def calculate_average_daily_return(prices, allocs):
    daily_returns = calculate_daily_returns(prices, allocs)
    return daily_returns.mean()

def calculate_standard_deviation_of_daily_returns(prices, allocs):
    daily_returns = calculate_daily_returns(prices, allocs)
    return daily_returns.std()

def calculate_sharpe_ratio(prices, allocs):
    adr = calculate_average_daily_return(prices, allocs)
    sddr = calculate_standard_deviation_of_daily_returns(prices, allocs)
    return (adr / sddr) * np.sqrt(252)  # Assuming 252 trading days in a year

def calculate_daily_returns(prices, allocs):
    normalized_prices = prices / prices.iloc[0]
    position_values = normalized_prices * allocs
    portfolio_value = position_values.sum(axis=1)
    daily_returns = portfolio_value.pct_change()
    return daily_returns[1:]

def calculate_daily_portfolio_value(prices, allocs):
    position_values = prices * allocs
    portfolio_value = position_values.sum(axis=1)
    return portfolio_value

def plot_normalized_portfolio(port_val, prices_SPY):
    df_temp = pd.concat([port_val, prices_SPY], keys=["Portfolio", "SPY"], axis=1)
    df_temp = df_temp / df_temp.iloc[0]
    plot_normalized_data(df_temp, title="Portfolio vs. SPY", ylabel="Normalized Price")
    plt.savefig('Figure1.png')


# Helper function to normalize data
def plot_normalized_data(df, title, ylabel, username='mwang611'):
    fig, ax = plt.subplots()
    df.plot(ax=ax, title=title, fontsize=12)
    ax.set_ylabel(ylabel)
    plt.xlabel('Date')
    plt.xticks(fontsize=8)
    if username:
        fig.text(
            0.5, 0.5,
            f'Username: {username}',
            ha='center',
            va='center',
            rotation=45,
            fontsize=24,
            color='Grey',
            alpha=0.5,
            bbox=dict(boxstyle="round,pad=0.3", edgecolor="none", facecolor="none")
        )

    plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.1)
    plt.savefig('Figure1.png', transparent=True)
    plt.show()


def test_code():
    start_date = dt.datetime(2008, 6, 1)
    end_date = dt.datetime(2009, 6, 1)
    symbols = ["IBM", "X", "GLD", "JPM"]

    allocations, cr, adr, sddr, sr = optimize_portfolio(
        sd=start_date, ed=end_date, syms=symbols, gen_plot=True
    )

    print(f"Start Date: {start_date}")
    print(f"End Date: {end_date}")
    print(f"Symbols: {symbols}")
    print(f"Allocations: {allocations}")
    print(f"Sharpe Ratio: {sr}")
    print(f"Volatility (stdev of daily returns): {sddr}")
    print(f"Average Daily Return: {adr}")
    print(f"Cumulative Return: {cr}")


if __name__ == "__main__":
    test_code()
