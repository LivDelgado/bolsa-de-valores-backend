#external
from fastapi import FastAPI, HTTPException
from starlette.middleware.cors import CORSMiddleware

#internal
import app.models.TimeSeries as time_series
import app.api.alpha_vantage as alpha
import app.models.constants as constants

app = FastAPI()

origins = [
    "https://bolsa-de-valores-livia-delgado.netlify.app",
    "https://bolsa-de-valores-livia-delgado.netlify.app/",
    "http://localhost:8080",
    "http://localhost:8080/",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"],
)

@app.get("/pontos-ibovespa")
async def pontos_ibovespa():
    bovespa = time_series.BovespaTimeSeries()
    bovespa.updates = await alpha.obter_variacoes_ibovespa()
    bovespa.info = await alpha.obter_informacoes_empresa(constants.BOVESPA)
    return bovespa

@app.get("/empresas")
async def listar_possiveis_empresas(nome_empresa: str):
    retorno_busca = await alpha.procurar_empresa(nome_empresa)
    if len(retorno_busca) == 0:
        raise HTTPException(
            status_code = 404,
            detail="Nenhuma empresa foi encontrada a partir do nome informado."
        )
    return retorno_busca

@app.get("/empresas/{simbolo}")
async def obter_empresa(simbolo: str):
    retorno = await alpha.obter_informacoes_empresa(simbolo)
    if (retorno == None):
        raise HTTPException(
            status_code = 404,
            detail="Nenhuma empresa foi encontrada a partir do símbolo informado."
        )
    else:
        return retorno