# src/utils/autenticacion.py
import os
import json
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from dotenv import load_dotenv
import src.config

load_dotenv()
globals = src.config

def guardar_credenciales_json():
    credentials_env = os.getenv("GOOGLE_CREDENTIALS")
    if not credentials_env:
        raise Exception("❌ No se encontró GOOGLE_CREDENTIALS en variables de entorno")

    ruta_credenciales = os.path.join(globals.RUTA_BASE, 'credentials.json')
    if not os.path.exists(ruta_credenciales):
        with open(ruta_credenciales, 'w') as f:
            json.dump(json.loads(credentials_env), f)
            print("✅ credentials.json generado desde GOOGLE_CREDENTIALS")

def obtener_servicio():
    SCOPES = ['https://www.googleapis.com/auth/gmail.send']
    token_path = os.path.join(globals.RUTA_BASE, 'token.json')

    guardar_credenciales_json()

    creds = None
    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                os.path.join(globals.RUTA_BASE, 'credentials.json'), SCOPES)
            creds = flow.run_local_server(port=0)

        with open(token_path, 'w') as token:
            token.write(creds.to_json())

    return build('gmail', 'v1', credentials=creds)

