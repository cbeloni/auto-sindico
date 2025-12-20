from fastapi.templating import Jinja2Templates

from dto.cobrar_request import CobrarRequest
from repository.fechamento_despesas import fechamento_despesas_pendentes, marcar_status, marcar_status_whatsapp
from service.email_service import enviar_email
from service.whatsapp_service import enviar_cobranca_whatsapp
from util.identificadores import email_mapping, telefone_mapping

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
        
def cobrar_e_enviar_whatsapp(fechamento_request: CobrarRequest):
    
    fechamentos_pendentes = fechamento_despesas_pendentes(mes=fechamento_request.mes, ano=fechamento_request.ano)
    
    for fechamento in fechamentos_pendentes:
    
        templates = Jinja2Templates(directory="templates")
        context = {
            "request": {},
            "apartamento": fechamento.apartamento,
            "mes": fechamento.mes,
            "valor": fechamento.valor,
            "codigo_pix": fechamento.brcode
        }

        body = templates.TemplateResponse("whatsapp_template.txt", context).body.decode("utf-8")

        enviar_cobranca_whatsapp(telefone=telefone_mapping.get(fechamento.apartamento), mensagem=body, imagem_url=f"https://br-se1.magaluobjects.com/qrcodepix/{fechamento.url_qrcode}", pix_code=fechamento.brcode)

        marcar_status_whatsapp(mes=fechamento.mes, ano=fechamento.ano, apartamento=fechamento.apartamento, status='enviado')