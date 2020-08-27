#external
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

#internal
import app.models.TimeSeries as time_series
import app.api.alpha_vantage as alpha
import app.models.constants as constants

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
    bovespa = time_series.BovespaTimeSeries()
    bovespa.atualizacoes = await alpha.obter_variacoes_ibovespa()
    bovespa.informacoes = await alpha.obter_informacoes_empresa(constants.BOVESPA)
    return bovespa
