from fastapi import FastAPI
from typing import List, Optional
from pydantic import BaseModel

import app.models.TimeSeries as time_series
from app.api.alpha_vantage import obter_pontos_ibovespa

app = FastAPI()

@app.get("/pontos-ibovespa")
async def pontos_ibovespa(response_model = time_series.BovespaTimeSeries):
    return await obter_pontos_ibovespa()
