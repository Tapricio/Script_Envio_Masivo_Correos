import base64
import os.path
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/gmail.send']

def obtener_servicio():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    else:
        flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    servicio = build('gmail', 'v1', credentials=creds)
    return servicio

def enviar_con_destinatario(servicio, destinatario, asunto, cuerpo_html):
    mensaje = {
        'to': destinatario,
        'subject': asunto,
        'body': cuerpo_html
    }

    raw_message = crear_mensaje_raw(mensaje)
    enviar_mensaje(servicio, raw_message)

def crear_mensaje_raw(mensaje):
    mensaje_texto = f"To: {mensaje['to']}\r\nSubject: {mensaje['subject']}\r\n\r\n{mensaje['body']}"
    mensaje_bytes = base64.urlsafe_b64encode(mensaje_texto.encode('utf-8'))
    return mensaje_bytes.decode('utf-8')

def enviar_mensaje(servicio, raw_message):
    message = servicio.users().messages().send(userId="me", body={'raw': raw_message}).execute()
    print('Mensaje enviado: %s' % message['id'])

if __name__ == '__main__':
    servicio = obtener_servicio()
    destinatario = 'soporteti@fcchc.cl'  # Especifica el correo aquí
    asunto = 'Correo de prueba'
    cuerpo_html = 'Este es el cuerpo del correo'
    enviar_con_destinatario(servicio, destinatario, asunto, cuerpo_html)
