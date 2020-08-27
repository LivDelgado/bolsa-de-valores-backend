from fastapi.testclient import TestClient
import pytest
import asyncio

import app.models.TimeSeries as models
from app.main import app

client = TestClient(app)

def test_pontos_ibovespa():
    response = client.get("/pontos-ibovespa")
    assert response.status_code == 200

def test_listar_possiveis_empresas_unprocessable_entity():
    response = client.get("/empresas")
    assert response.status_code == 422

def test_listar_possiveis_empresas_not_found(mocker):
    future = asyncio.Future()
    future.set_result([])
    mocker.patch('app.api.alpha_vantage.procurar_empresa', return_value=future)
    response = client.get("/empresas?nome_empresa=teste")
    assert response.status_code == 404

def test_listar_possiveis_empresas_success(mocker):
    future = asyncio.Future()
    future.set_result([models.EnterpriseMatch(), models.EnterpriseMatch()])
    mocker.patch('app.api.alpha_vantage.procurar_empresa', return_value=future)
    response = client.get("/empresas?nome_empresa=teste")
    assert response.status_code == 200

def test_obter_empresa_unprocessable_entity():
    response = client.get("/empresas/")
    assert response.status_code == 422

def test_obter_empresa_not_found(mocker):
    future = asyncio.Future()
    future.set_result(None)
    mocker.patch('app.api.alpha_vantage.obter_informacoes_empresa', return_value=future)
    response = client.get("/empresas/simbolo_teste")
    assert response.status_code == 404

def test_obter_empresa_success(mocker):
    future = asyncio.Future()
    future.set_result(models.EnterpriseInfo())
    mocker.patch('app.api.alpha_vantage.obter_informacoes_empresa', return_value=future)
    response = client.get("/empresas/simbolo_teste")
    assert response.status_code == 200
