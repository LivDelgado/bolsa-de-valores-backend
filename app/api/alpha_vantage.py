import time
import requests
from typing import List

import app.config as config
import app.models.TimeSeries as time_series
import app.models.constants as constants

def convert_string_value_to_float(value):
    s = value[:-1].replace('.', '') + '.' + value[-1:]
    return float(s)

def convert_time_series(to_convert):
    updates = []
    time_series_daily = to_convert.get("Time Series (Daily)", [])
    if (len(time_series_daily) == 0):
        return updates
    count = 0
    for day in time_series_daily:
        if count < 10:
            update = time_series.TimeEntry()
            update.date = day
            update.value = convert_string_value_to_float(time_series_daily[day]['4. close'])
            updates.append(update)
        count += 1
    return updates

def convert_enterprise_info(to_convert): 
    enterprise = time_series.EnterpriseInfo()
    data = to_convert.get("Global Quote", [])
    if (len(data) == 0):
        return None
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

def converter_enterprise_matches(to_convert):
    best_matches = to_convert.get("bestMatches", [])
    if (len(best_matches) == 0):
        return []
    enterprise_matches = []
    if len(best_matches) == 0:
        return []
    else:
        for match in best_matches:
            enterprise_match = time_series.EnterpriseMatch()
            enterprise_match.symbol = match["1. symbol"]
            enterprise_match.name = match["2. name"]
            enterprise_match.match_score = match["9. matchScore"]
            enterprise_matches.append(enterprise_match)
        return enterprise_matches

async def obter_variacoes_ibovespa():
    data = { 
        "datatype": "json",
        "function": "TIME_SERIES_DAILY", 
        "symbol": constants.BOVESPA
    }
    response = requests.get(config.API_URL, params = data)
    return convert_time_series(response.json())

async def obter_informacoes_empresa(symbol):
    data = {
        "datatype": "json",
        "function": "GLOBAL_QUOTE", 
        "symbol": symbol
    }
    time.sleep(15)
    response = requests.get(config.API_URL, params = data)
    return convert_enterprise_info(response.json())

async def procurar_empresa(nome_empresa):
    data = {
        "datatype": "json",
        "function": "SYMBOL_SEARCH", 
        "keywords": nome_empresa
    }
    time.sleep(15)
    response = requests.get(config.API_URL, params = data)
    return converter_enterprise_matches(response.json())
