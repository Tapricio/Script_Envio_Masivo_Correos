# Autenticación y creación del servicio
import os
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
import src.config

globals = src.config
def obtener_servicio():
    SCOPES = ['https://www.googleapis.com/auth/gmail.send']

    creds = None
    token_path = os.path.join(globals.RUTA_BASE,'token.json')
    #if os.path.exists('token.json'):
    if os.path.exists(token_path):
        #creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)

        #with open('token.json', 'w') as token:
        with open(token_path, 'w') as token:
            token.write(creds.to_json())

    return build('gmail', 'v1', credentials=creds)
