from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.requests import Request
from dto.cobrar_request import CobrarRequest
from dto.email import EmailRequest
from dto.extrato_request import ExtratoApiRequest
from dto.fechamento_requests import (
    FechamentoDespesasRequest,
    FechamentoRequest,
    FechamentoPagamentosDate,
)
from dto.pagbank_request import MovimentosPagbankParams
from dto.pix import PixRequest
from dto.resumo_requests import ResumoRequest
from dto.totalizacao import calcular_totais
from repository.caixa import caixa_ordenado_por_id_desc
from repository.concialicao import concialiacao_ordenadas_por_id_desc
from repository.despesas import despesas_ordenadas_por_id_desc
from service.cobrar_service import cobrar_e_enviar_email
from service.drive_service import get_last_file_from_drive
from service.email_service import enviar_email, read_emails_from_gmail
from service.extrato.factory_extrato import factory_extrato_service
from service.fechamento_despesas import fechar_despesas
from service.fechamento_pagamento import fechar_pagamentos
from service.message_whatsapp import montar_messagem_whatsapp
from service.qrcode_service import generate_qrcode
from service.resumo import consultar_tipo_transacao
from service.send_whatsapp import send_whatsapp_message
from service.extrato.extrato_abstract import ExtratoAbstract
from service.cobrar_service import cobrar_e_enviar_whatsapp
    
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
def drive() -> list:
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


@app.post("/extrato")
def extrato(request: ExtratoApiRequest = None) -> dict:
    if request is None:
        request = ExtratoApiRequest()
    extrato: ExtratoAbstract = factory_extrato_service(request.provider)
    extrato_dados = extrato.obter_extrato(request.data_inicial, request.data_final)
    if request.gravar:
        extrato.gravar_extrato(extrato_dados)
    return extrato_dados


@app.post("/fechamento-despesas")
def fechamento_despesas(request: FechamentoDespesasRequest = None) -> dict:
    if request is None:
        request = FechamentoDespesasRequest()
    return fechar_despesas(request.data_inicial, request.data_final)


@app.post("/fechamento-pagamentos")
def fechamento_pagamentos(request: FechamentoRequest = None) -> dict:
    if request is None:
        request = FechamentoPagamentosDate()
    return fechar_pagamentos(request.data_inicial, request.data_final)


@app.get("/", response_class=HTMLResponse)
async def read_home(request: Request):
    despesas = concialiacao_ordenadas_por_id_desc()
    totais = calcular_totais(despesas)
    return templates.TemplateResponse(
        "home.html", {"request": request, "despesas": despesas, **totais}
    )


@app.post("/qrcode")
def qrcode(
    request: PixRequest = PixRequest(
        name_receiver="Cauê Beloni",
        city_receiver="Santo André",
        key="cbeloni@gmail.com",
        identification="12345",
        zipcode_receiver="09291250",
        description="condominio mensal",
        amount=1.0,
    ),
) -> dict:
    return generate_qrcode(request)


@app.post("/send-email")
def send_email(request: EmailRequest) -> dict:
    enviar_email(request.subject, request.body, request.recipient)
    return {"message": "Email sent successfully"}


@app.post("/send-whatsapp")
def send_whatsapp(numero: str = "5511941503226") -> dict:
    transacoes = concialiacao_ordenadas_por_id_desc()
    mensagens = montar_messagem_whatsapp(transacoes)
    for mensagem in mensagens:
        send_whatsapp_message(numero, mensagem)
    return {"message": "Mensagens enviadas com sucesso"}


@app.post("/cobrar")
def cobrar(request: CobrarRequest = CobrarRequest()) -> dict:
    cobrar_e_enviar_email(request)
    return {"message": "Email sent successfully"}

@app.post("/cobrar-whatsapp")
def cobrar_whatsapp(request: CobrarRequest = CobrarRequest()) -> dict:
    cobrar_e_enviar_whatsapp(request)
    return {"message": "WhatsApp messages sent successfully"}

@app.post("/resumo")
def resumo(request: ResumoRequest = None):
    if request is None:
        request = ResumoRequest()
    return consultar_tipo_transacao(request)


@app.post("/movimentos-pagbank")
def movimentos_pagbank(request: MovimentosPagbankParams):
    from integrations.pagbank import consultar_movimentos_pagbank

    response = consultar_movimentos_pagbank(
        data_movimento=request.data_movimento,
        page_number=request.page_number,
        page_size=request.page_size,
        tipo_movimento=request.tipo_movimento,
    )

    if response is None:
        return {"error": "Erro ao consultar movimentos PagBank"}

    return {"status_code": response.status_code, "data": response.json()}
