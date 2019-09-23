import requests
import json
from datetime import datetime
from dateutil.relativedelta import relativedelta

def tickerData(ticker):
    url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol=' + ticker + '&outputsize=full&apikey=GR21IK406A44A99H'
    url_request = requests.get(url)
    text = url_request.text
    text_output = json.loads(text)

    adj_close = []
    adj_close_final = []
    keys = []
    keys_initial = list(text_output['Time Series (Daily)'].keys())
    five_yrs_raw = str(datetime.now() - relativedelta(years=5))
    five_yrs = five_yrs_raw[:10]

    for date_value in range(len(keys_initial)):
        if keys_initial[date_value] == five_yrs:
            stoplimit = date_value + 1
            for i in range(len(keys_initial[:stoplimit])):
                keys.append(keys_initial[i])

    for date in range(len(keys)):
        adj_close.append(text_output['Time Series (Daily)'][keys[date]]['5. adjusted close'])

    for value in range(1, len(adj_close) + 1):
        adj_close_final.append(float(adj_close[-value]))

    return adj_close_final

def IndexData():
    url = 'https://www.alphavantage.co/query?function=TIME_SERIES_DAILY_ADJUSTED&symbol=SPX&outputsize=full&apikey=GR21IK406A44A99H'
    url_request = requests.get(url)
    text = url_request.text
    text_output = json.loads(text)

    adj_close = []
    adj_close_final = []
    keys = []
    keys_initial = list(text_output['Time Series (Daily)'].keys())
    five_yrs_raw = str(datetime.now() - relativedelta(years=5))
    five_yrs = five_yrs_raw[:10]

    for date_value in range(len(keys_initial)):
        if keys_initial[date_value] == five_yrs:
            stoplimit = date_value + 1
            for i in range(len(keys_initial[:stoplimit])):
                keys.append(keys_initial[i])

    for date in range(len(keys)):
        adj_close.append(text_output['Time Series (Daily)'][keys[date]]['5. adjusted close'])

    for value in range(1, len(adj_close) + 1):
        adj_close_final.append(float(adj_close[-value]))

    return adj_close_final

IndexData()