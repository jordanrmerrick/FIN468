import pandas as pd
import numpy as np
import requests
import json
from scipy import stats



def historicalDataGet(ticker):
    url = 'https://api.worldtradingdata.com/api/v1/history?symbol=' + ticker + '&sort=newest&api_token=i0IqIaBJau36El9cM41zCxS4guNb7aBrJk3hBWfpzvPAQM9rVwhty70TvjVJ&date_from=2014-09-20'
    url_request = requests.get(url)
    text = url_request.text
    xlss = json.loads(text)

    prices = []
    prices_final = []
    keys = list(xlss['history'].keys())
    for i in range(len(keys)):
        prices.append(xlss['history'][keys[i]]['close'])

    for k in range(len(prices)):
        prices_final.append(float(prices[k]))

    return prices_final

def covariance(prices, prices_index):
    percent_change = []
    percent_change_index = []
    averages_pc = []
    averages_pci = []
    average = []

    if len(prices) != len(prices_index):
        raise ValueError

    n = len(prices)
    for value in range(1, len(prices)):
        percent_change.append((prices[-value - 1] - prices[-value]) / prices[-value])

    for index_value in range(1, len(prices_index)):
        percent_change_index.append(
            (prices_index[-index_value - 1] - prices_index[-index_value]) / prices_index[-index_value])

    avg_x = sum(percent_change)/n
    avg_y = sum(percent_change_index)/n

    for x in range(len(percent_change)):
        averages_pc.append(percent_change[x] - avg_x)
    for y in range(len(percent_change_index)):
        averages_pci.append(percent_change[y] - avg_y)

    for z in range(len(percent_change)):
        average.append(averages_pc[z]*averages_pci[z])

    covar = (1/(n-1))*sum(average)

    print(covar/np.var(percent_change_index))

def statisticalMethods(ticker, prices, prices_index):
    percent_change = []
    percent_change_index = []

    for value in range(1, len(prices)):
        percent_change.append((prices[-value - 1] - prices[-value])/prices[-value])

    for index_value in range(1, len(prices_index)):
        percent_change_index.append((prices_index[-index_value - 1] - prices_index[-index_value])/prices_index[-index_value])

    variance = np.var(percent_change_index)
    slope, intercept, r_value, p_value, std_err = stats.linregress(percent_change, percent_change_index)
    covar = np.cov(percent_change, percent_change_index)
    print(slope)
    print(covar)
    print(slope/variance)

# statisticalMethods('IT', historicalDataGet('IT'), historicalDataGet('SPY'))
covariance(historicalDataGet('IT'), historicalDataGet('SPY'))