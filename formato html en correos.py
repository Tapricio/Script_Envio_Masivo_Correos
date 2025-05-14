import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
from urllib.request import Request
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

# Autenticación y creación del servicio
def obtener_servicio():
    SCOPES = ['https://www.googleapis.com/auth/gmail.send']

    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)

        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    return build('gmail', 'v1', credentials=creds)

# Función para enviar el correo
def enviar_con_destinatario(servicio, destinatario, asunto, cuerpo_html):
    # Crear un mensaje MIME
    mensaje = MIMEMultipart()
    mensaje['To'] = destinatario
    mensaje['Subject'] = asunto

    # Adjuntar el cuerpo del mensaje en formato HTML
    mensaje.attach(MIMEText(cuerpo_html, 'html'))

    # Convertir el mensaje a formato raw (base64)
    raw_message = base64.urlsafe_b64encode(mensaje.as_bytes()).decode('utf-8')

    # Enviar el mensaje
    try:
        servicio.users().messages().send(userId="me", body={'raw': raw_message}).execute()
        print("Correo enviado exitosamente.")
    except Exception as error:
        print(f"Ha ocurrido un error: {error}")

# Crear el contenido del correo en formato HTML
def generar_contenido_html():
    cuerpo_html = """
    <p style="color: blue; font-weight: bold;">Este es un mensaje de prueba con formato HTML.</p>
    <p style="font-size: 18px;">Puedes incluir <strong>negrita</strong>, <span style="color: red;">colores</span>, y <em>cursiva</em>.</p>
    """

    # Firma en HTML
    firma = """
    <br><br>
    <hr>
    <p style="color: green; font-weight: bold;">Saludos,<br>Patricio Torres</p>
    <p><a href="http://www.tusitio.com" style="color: green;">www.tusitio.com</a></p>
    """

    # Concatenar cuerpo con la firma
    cuerpo_html_con_firma = cuerpo_html + firma

    return cuerpo_html_con_firma

# Llamada principal
def main():
    servicio = obtener_servicio()
    destinatario = "soporteti@fcchc.cl"
    asunto = "Correo de prueba con firma y formato HTML"
    
    cuerpo_html_con_firma = generar_contenido_html()

    # Enviar el correo
    enviar_con_destinatario(servicio, destinatario, asunto, cuerpo_html_con_firma)

if __name__ == '__main__':
    main()
