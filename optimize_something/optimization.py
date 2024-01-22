
import datetime as dt

import numpy as np

import matplotlib.pyplot as plt
import scipy.optimize as spo
import pandas as pd
from util import get_data, plot_data


# This is the function that will be tested by the autograder
# The student must update this code to properly implement the functionality
def get_portfolio(prices, alloc, initial_amount):
    # Normalize values
    temp_prices = prices/prices.iloc[0]
    temp_prices = temp_prices * alloc
    temp_prices = temp_prices * initial_amount
    # daily_total_value ---->  portfolio
    portfolio_values = temp_prices.sum(axis = 1)
    return portfolio_values



def cal_daily_returns(portfolio_values):
	dailyReturns = portfolio_values.copy()
	dailyReturns[1:] = portfolio_values[1:]/(portfolio_values[:-1].values) - 1
	dailyReturns = dailyReturns[1:]
	return dailyReturns

def cal_avg_daily_returns(daily_returns):
	return daily_returns.mean()

def cal_std_daily_returns(daily_returns):
	return daily_returns.std()

def sum_cummulative_returns(portfolio_values):
	return (portfolio_values[-1]/portfolio_values[0]) - 1

def opt_sharpe_ratio(daily_returns):
	return np.sqrt(252) * cal_avg_daily_returns(daily_returns)/cal_std_daily_returns(daily_returns)


def cal_minimize_sharpe_ratio(alloc, prices):


	portfolio_values = get_portfolio(prices, alloc, 1)
	dailyReturns = cal_daily_returns(portfolio_values)
	sharpe_ratio = opt_sharpe_ratio(dailyReturns)


    # need to be Negative
	return (-1)*sharpe_ratio


# This is the function that will be tested by the autograder
# The student must update this code to properly implement the functionality
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
    # note that the values here ARE NOT meant to be correct for a test case

    # the number_of_stocks ---> len(syms)
    allocs = [1.0 / len(syms)] * len(syms)
    allocs = np.asarray(allocs)
    bounds = [(0.0, 1.0)] * len(syms)
    constraint = [{'type': 'eq', 'fun': lambda x:np.sum(x)-1}]  # linear_constraint---->  np.sum(x) - 1

    min_result = spo.minimize(cal_minimize_sharpe_ratio, allocs, method='SLSQP', args=(prices), bounds=bounds, constraints=constraint)

    alloc_optimized = min_result.x

    portfolio_values = get_portfolio(prices, alloc_optimized, 1)
    DR = cal_daily_returns(portfolio_values)
    ADR = cal_avg_daily_returns(DR)
    CR = sum_cummulative_returns(portfolio_values)
    SDDR = cal_std_daily_returns(DR)
    SR = opt_sharpe_ratio(DR)


    # Get daily portfolio value
    port_val = portfolio_values  # add code here to compute daily portfolio values

    # Compare daily portfolio value with SPY using a normalized plot
    if gen_plot:
        # add code to plot here
        df_temp = pd.concat([port_val, prices_SPY], keys=["Portfolio", "SPY"], axis=1)
        plot_normalized_data(df_temp, title="Portfolio vs. SPY", ylabel="Normalized Price")
        plt.xlabel('Date')
        plt.ylabel('Price')
        plt.title('Daily Portfolio Value and SPY')
        plt.text(
            port_val.index[-1],
            port_val.iloc[-1]['Portfolio'],
            f'Username: {username}',
            verticalalignment='bottom',
            horizontalalignment='right',
            color='red',
            fontsize=8
        )
        plt.savefig('Figure1.png')
        pass

    return alloc_optimized, CR, ADR, SDDR, SR


def test_code():
    """
    This function WILL NOT be called by the auto grader.
    """

    start_date = dt.datetime(2008, 6, 1)
    end_date = dt.datetime(2009, 6, 1)
    symbols = ["IBM", "X", "GLD","JPM"]

    # Assess the portfolio
    allocations, cr, adr, sddr, sr = optimize_portfolio(
        sd=start_date, ed=end_date, syms=symbols, gen_plot = True
    )

    # Print statistics
    print(f"Start Date: {start_date}")
    print(f"End Date: {end_date}")
    print(f"Symbols: {symbols}")
    print(f"Allocations:{allocations}")
    print(f"Sharpe Ratio: {sr}")
    print(f"Volatility (stdev of daily returns): {sddr}")
    print(f"Average Daily Return: {adr}")
    print(f"Cumulative Return: {cr}")


if __name__ == "__main__":
    # This code WILL NOT be called by the auto grader
    # Do not assume that it will be called
    test_code()
