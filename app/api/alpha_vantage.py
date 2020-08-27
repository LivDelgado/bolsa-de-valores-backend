import requests
from typing import List

import app.config as config
import app.models.TimeSeries as time_series
import app.models.constants as constants

def convert_string_value_to_float(value):
    s = value[:-1].replace('.', '') + '.' + value[-1:]
    return float(s)

def converter_time_series(to_convert):
    updates = []
    time_series_daily = to_convert['Time Series (Daily)']
    count = 0
    for day in time_series_daily:
        if count < 10:
            update = time_series.TimeEntry()
            update.date = day
            update.value = convert_string_value_to_float(time_series_daily[day]['4. close'])
            updates.append(update)
        count += 1
    return updates

def converter_enterprise_info(to_convert): 
    enterprise = time_series.EnterpriseInfo()
    data = to_convert["Global Quote"]
    enterprise.symbol = data["01. symbol"]
    enterprise.open_value = convert_string_value_to_float(data["02. open"])
    enterprise.high_value = convert_string_value_to_float(data["03. high"])
    enterprise.low_value = convert_string_value_to_float(data["04. low"])
    enterprise.price_value = convert_string_value_to_float(data["05. price"])
    enterprise.volume_value = float(data["06. volume"])
    enterprise.date = data["07. latest trading day"]
    enterprise.previous_close = convert_string_value_to_float(data["08. previous close"])
    enterprise.change = data["09. change"]
    enterprise.change_percentage = data["10. change percent"]
    return enterprise

async def obter_variacoes_ibovespa():
    data = { 
        "datatype": "json",
        "function": "TIME_SERIES_DAILY", 
        "symbol": constants.BOVESPA
    }
    response = requests.get(config.API_URL, params = data)
    return converter_time_series(response.json())

async def obter_informacoes_empresa(symbol):
    data = {
        "datatype": "json",
        "function": "GLOBAL_QUOTE", 
        "symbol": symbol
    }
    response = requests.get(config.API_URL, params = data)
    return converter_enterprise_info(response.json())