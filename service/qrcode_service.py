from pypix.pix import Pix

from dto.pix import PixRequest

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
    
    return {'qrcode': base64qr, 'br_code': pix.get_br_code()}




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