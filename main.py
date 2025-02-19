from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.requests import Request
from dto.fechamento_requests import FechamentoRequest
from repository.caixa import caixa_ordenado_por_id_desc
from repository.concialicao import concialiacao_ordenadas_por_id_desc
from repository.despesas import despesas_ordenadas_por_id_desc
from service.drive_service import get_last_file_from_drive
from service.email_service import read_emails_from_gmail
from service.fechamento_despesas import fechar_despesas
from pydantic import BaseModel

from service.fechamento_pagamento import fechar_pagamentos
app = FastAPI()
templates = Jinja2Templates(directory="templates")


# About page route
@app.get("/about")
def about() -> dict[str, str]:
    return {"message": "This is the about page."}

@app.get("/mail")
def mail() -> list:
    return read_emails_from_gmail()

@app.get("/drive")
def mail() -> list:
    return get_last_file_from_drive()

@app.get("/despesas")
def despesas() -> list:
    return despesas_ordenadas_por_id_desc()

@app.get("/caixa")
def caixa() -> list:
    return caixa_ordenado_por_id_desc()

@app.get("/concialiacao")
def concialiacao() -> list:
    return concialiacao_ordenadas_por_id_desc()

@app.post("/fechamento-despesas")
def fechamento(request: FechamentoRequest = FechamentoRequest()) -> dict:
    return fechar_despesas(request.data_inicial, request.data_final)

@app.post("/fechamento-pagamentos")
def fechamento(request: FechamentoRequest = FechamentoRequest()) -> dict:
    return fechar_pagamentos(request.data_inicial, request.data_final)

@app.get("/", response_class=HTMLResponse)
async def read_home(request: Request):
    despesas = concialiacao_ordenadas_por_id_desc()
    return templates.TemplateResponse("home.html", {"request": request, "despesas": despesas})