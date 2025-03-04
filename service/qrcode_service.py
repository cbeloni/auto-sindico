from pypix.pix import Pix

from dto.pix import PixRequest
from repository.fechamento_despesas import FechamentoDespesas
from service.bucket import enviar_base64
from datetime import datetime

def generate_qrcode(pix_data: PixRequest) -> dict:
    pix = Pix()
    pix.set_name_receiver(pix_data.name_receiver)
    pix.set_city_receiver(pix_data.city_receiver)
    pix.set_key(pix_data.key)
    pix.set_identification(pix_data.identification)
    pix.set_zipcode_receiver(pix_data.zipcode_receiver)
    pix.set_description(pix_data.description)
    pix.set_amount(pix_data.amount)

    # print('\nDonation with defined amount - PYPIX >>>>\n', pix.get_br_code())
    
    base64qr = pix.save_qrcode(
        './qrcode.png',
        color="black",
        box_size=7,
        border=1,
    )
      
    current_date = datetime.now().strftime("%Y%m%d%H%M%S")
    nome_arquivo = f"qrcode-{pix_data.identification}-{current_date}.png"
    enviar_base64("qrcodepix", base64qr.replace("data:image/png;base64,", ""), nome_arquivo, "image/png")
    
    return {'qrcode': base64qr, 'br_code': pix.get_br_code(), 'nome_arquivo': nome_arquivo}

def gerar_salvar_qrcode(mes, ano, apartamento, identification, description, amount):
    pix = PixRequest(
        name_receiver='Cauê Beloni',
        city_receiver='Santo André',
        key='11986768497',
        identification=identification,
        zipcode_receiver='09291250',
        description=description,
        amount=amount
    )
    pix_response = generate_qrcode(pix)
    fechamento_despesas = FechamentoDespesas(
        mes=mes, 
        ano=ano, 
        apartamento=apartamento,
        valor=amount, 
        brcode=pix_response.get("br_code"), 
        qrcode=pix_response.get("qrcode"), 
        url_qrcode=pix_response.get("nome_arquivo")
    )
    fechamento_despesas.save()


# Exemplo de uso
if __name__ == "__main__":
    def normal_static():
        pix = Pix()
        pix.set_name_receiver('Cauê Beloni')
        pix.set_city_receiver('Santo André')
        pix.set_key('cbeloni@gmail.com')
        pix.set_identification('12345')
        pix.set_zipcode_receiver('09291250')
        pix.set_description('condominio mensal')
        pix.set_amount(1.0)

        # print('\nDonation with defined amount - PYPIX >>>>\n', pix.get_br_code())
        
        base64qr = pix.save_qrcode(
            './qrcode.png',
            color="black",
            box_size=7,
            border=1,
        )
        
        return {'qrcode': base64qr, 'br_code': pix.get_br_code()}

        # pix.qr_ascii() 
        # if base64qr:  # Imprime qrcode em fomato base64
        #     print('Success in saving static QR-code.')
        #     print(base64qr)
        # else:
        #     print('Error saving QR-code.')
        normal_static()