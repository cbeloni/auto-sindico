import boto3
import os 
from dotenv import load_dotenv
import base64
from io import BytesIO

load_dotenv()

AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
ENDPOINT_URL = os.environ.get('ENDPOINT_URL')


_s3_client = boto3.client('s3',
                          aws_access_key_id=AWS_ACCESS_KEY_ID,
                          aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                          endpoint_url=ENDPOINT_URL)

def enviar(bucket_name: str, file_path: str, object_name: str, content_type: str, ):
    extra_args = {'ContentType': content_type}
    _s3_client.upload_file(file_path, bucket_name, object_name, ExtraArgs=extra_args)
    

def enviar_base64(bucket_name: str, base64_string: str, object_name: str, content_type: str):
    image_data = base64.b64decode(base64_string)
    _s3_client.put_object(
        Bucket=bucket_name,
        Key=object_name,
        Body=image_data,
        ContentType='image/png'
    )
        

def list_buckets():
    response = _s3_client.list_buckets()
    buckets = [bucket['Name'] for bucket in response['Buckets']]
    print("Listando buckets...")
    for bucket in buckets:
        print(bucket)


if __name__ == '__main__':
    imagem_base64 = """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"""
    enviar_base64('qrcodepix', imagem_base64, 'qrcore-janeiro-2025-ap1.png', 'image/png')
    
    list_buckets()
    # enviar('qrcodepix',
    #         f"/home/caue/Documentos/auto-sindico/service/logo_pensi_V2.PNG",
    #         "logo_pensi_V3",
    #         'image/png')    
        