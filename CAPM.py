import pandas as pd
import numpy as np
from scipy import stats
import POST_Request_Ticker_Index as ti

def marketReturn(index):
    percent_change = []
    for index_value in range(1, len(index)):
        percent_change.append((index[index_value] - index[index_value - 1]) / index[index_value - 1])

    return (((1 + sum(percent_change)/len(percent_change)) ** 365) - 1)

def beta(prices, index):

    # Call all lists needed
    percent_change = []
    percent_change_index = []
    averages_pc = []
    averages_pci = []
    product = []
    varsquare = []

    # Initial test
    if len(prices) != len(index):
        raise ValueError

    n = len(prices)

    for value in range(1, len(prices)):
        percent_change.append((prices[value] - prices[value - 1]) / prices[value - 1])

    for index_value in range(1, len(index)):
        percent_change_index.append((index[index_value] - index[index_value - 1]) / index[index_value - 1])

    avg_x = sum(percent_change)/n
    avg_y = sum(percent_change_index)/n

    # Calculates the average (xi - xbar) - VERIFIED
    for x in range(len(percent_change)):
        averages_pc.append(percent_change[x] - avg_x)

    # Calculates the average (yi - ybar) - VERIFIED
    for y in range(len(percent_change_index)):
        averages_pci.append(percent_change_index[y] - avg_y)

    # Calculates product of (xi - xbar)*(yi - ybar)
    for z in range(len(percent_change)):
        product.append(averages_pc[z]*averages_pci[z])

    for j in range(len(percent_change_index)):
        varsquare.append((percent_change_index[j] - avg_y) ** 2)

    # Variance is verified
    variance = (1/n)*sum(varsquare)
    covar = (1/(n - 1))*sum(product)
    beta = covar/variance

    return beta


def CAPM(ticker):

    asset_beta = beta(ti.tickerData(ticker), ti.IndexData())
    risk_free_rate = ti.RiskFreeRate()
    market_return = marketReturn(ti.IndexData())

    print('The expected return of {} is {}%.'.format(ticker, round((risk_free_rate + asset_beta*(market_return - risk_free_rate))*100, 4)))

CAPM('AMZN')