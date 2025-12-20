import json
import os
import requests
from dotenv import load_dotenv
import base64

load_dotenv()
USER = os.getenv("WHATSAPP_USER")
PASSWORD = os.getenv("WHATSAPP_PASS")
WHATSAPP_API = os.getenv("WHATSAPP_API_URL")

def send_whatsapp_message(number: str, message: str):

    if not USER or not PASSWORD:
        raise ValueError("Usuário ou senha não encontrados no .env")

    auth = f"{USER}:{PASSWORD}"
    auth_b64 = base64.b64encode(auth.encode()).decode()

    url = f"{WHATSAPP_API}/sendmessage"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Basic {auth_b64}"
    }
    payload = {
        "number": number,
        "message": message
    }
    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()
    
def send_whatsapp_image(number: str, image_url: str, caption: str = ""):
    
    if not USER or not PASSWORD:
        raise ValueError("Usuário ou senha não encontrados no .env")

    auth = f"{USER}:{PASSWORD}"
    auth_b64 = base64.b64encode(auth.encode()).decode()

    url = f"{WHATSAPP_API}/sendimage"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Basic {auth_b64}"
    }
    payload = {
        "number": number,
        "imageUrl": image_url,
        "caption": caption
    }
    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()