import requests

import app.config as config
import app.models.TimeSeries as time_series

def converter_bovespa_time_series(to_convert):
    print(to_convert)
    bovespa = time_series.BovespaTimeSeries();
    metadata = to_convert['Meta Data']
    bovespa.ultima_atualizacao = metadata['3. Last Refreshed']
    bovespa.simbolo = metadata['2. Symbol']
    time_series_daily = to_convert['Time Series (Daily)']
    for day in time_series_daily:
        atualizacao = time_series.TimeEntry()
        atualizacao.data = day
        atualizacao.open_value = time_series_daily[day]['1. open']
        atualizacao.high_value = time_series_daily[day]['2. high']
        atualizacao.low_value = time_series_daily[day]['3. low']
        atualizacao.close_value = time_series_daily[day]['4. close']
        atualizacao.volume_value = time_series_daily[day]['5. volume']
        bovespa.atualizacoes.append(atualizacao)
    return bovespa

async def obter_pontos_ibovespa():
    data = { 
        "datatype": "json",
        "function": "TIME_SERIES_DAILY", 
        "symbol": "BOVV11.SAO"
    }
    response = requests.get(config.API_URL, params = data)
    return converter_bovespa_time_series(response.json())