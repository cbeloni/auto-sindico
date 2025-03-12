from fastapi.templating import Jinja2Templates

from dto.cobrar_request import CobrarRequest
from repository.fechamento_despesas import fechamento_despesas_pendentes, marcar_status
from service.email_service import enviar_email
from util.identificadores import email_mapping

def cobrar_e_enviar_email(fechamento_request: CobrarRequest):
    
    fechamentos_pendentes = fechamento_despesas_pendentes(mes=fechamento_request.mes, ano=fechamento_request.ano)
    
    for fechamento in fechamentos_pendentes:
    
        templates = Jinja2Templates(directory="templates")
        context = {
            "request": {},
            "mes": fechamento.mes,
            "valor": fechamento.valor,
            "codigo_pix": fechamento.brcode,
            "imagem_url": f"https://br-se1.magaluobjects.com/qrcodepix/{fechamento.url_qrcode}"
        }

        body = templates.TemplateResponse("email.html", context).body.decode("utf-8")
        assunto = f'Cobrança {fechamento.apartamento} - {fechamento.mes}.{fechamento.ano}'        
        email = email_mapping.get(fechamento.apartamento, 'cbeloni@gmail.com')              
        
        enviar_email(subject=assunto, body=body, to_email= email)
        
        marcar_status(mes=fechamento.mes, ano=fechamento.ano, apartamento=fechamento.apartamento, status='enviado')