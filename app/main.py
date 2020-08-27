from fastapi import FastAPI
from typing import List, Optional
from pydantic import BaseModel

from fastapi.middleware.cors import CORSMiddleware

import app.models.TimeSeries as time_series
from app.api.alpha_vantage import obter_pontos_ibovespa

app = FastAPI()

origins = [
    "https://bolsa-de-valores-livia-delgado.netlify.app",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/pontos-ibovespa")
async def pontos_ibovespa(response_model = time_series.BovespaTimeSeries):
    return await obter_pontos_ibovespa()
