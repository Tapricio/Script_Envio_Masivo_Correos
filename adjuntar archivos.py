import base64
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.base import MIMEBase
from email import encoders
from urllib.request import Request
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
import os

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
def enviar_con_destinatario(servicio, destinatario, asunto, cuerpo_html, imagen_path, archivo_path):
    # Crear un mensaje MIME
    mensaje = MIMEMultipart()
    mensaje['To'] = destinatario
    mensaje['Subject'] = asunto

    # Adjuntar el cuerpo del mensaje en formato HTML
    mensaje.attach(MIMEText(cuerpo_html, 'html'))

    # Adjuntar imagen embebida con CID
    if imagen_path:
        with open(imagen_path, 'rb') as img:
            imagen = MIMEImage(img.read())
            imagen.add_header('Content-ID', '<imagen_cid>')  # Usar un CID único para la imagen
            mensaje.attach(imagen)

    # Adjuntar archivo (puede ser cualquier tipo de archivo)
    if archivo_path:
        with open(archivo_path, 'rb') as archivo:
            adjunto = MIMEBase('application', 'octet-stream')
            adjunto.set_payload(archivo.read())
            encoders.encode_base64(adjunto)  # Codifica el archivo en base64
            adjunto.add_header('Content-Disposition', 'attachment', filename=os.path.basename(archivo_path))
            mensaje.attach(adjunto)

    # Convertir el mensaje a formato raw (base64)
    raw_message = base64.urlsafe_b64encode(mensaje.as_bytes()).decode('utf-8')

    # Enviar el mensaje
    try:
        servicio.users().messages().send(userId="me", body={'raw': raw_message}).execute()
        print("Correo enviado exitosamente.")
    except Exception as error:
        print(f"Ha ocurrido un error: {error}")

# Crear el contenido del correo en formato HTML con imagen embebida
def generar_contenido_html():
    cuerpo_html = """
    <p style="color: blue; font-weight: bold;">Este es un mensaje de prueba con formato HTML.</p>
    <p style="font-size: 18px;">Puedes incluir <strong>negrita</strong>, <span style="color: red;">colores</span>, y <em>cursiva</em>.</p>
    <p>Y aquí va la imagen embebida:</p>
    <img src="cid:imagen_cid" alt="Imagen" style="width: 150px; height: auto;" />
    """

    # Firma en HTML
    firma = """
    <br><br>
    <hr>
    <p style="color: green; font-weight: bold;">Saludos,<br>Patricio Torres</p>
    """

    # Concatenar cuerpo con la firma
    cuerpo_html_con_firma = cuerpo_html + firma

    return cuerpo_html_con_firma

# Llamada principal
def main():
    servicio = obtener_servicio()
    destinatario = "soporteti@fcchc.cl"
    asunto = "Correo de prueba con firma, imagen y archivo adjunto"
    
    cuerpo_html_con_firma = generar_contenido_html()
    imagen_path = 'img.png'  # Ruta a tu imagen local
    archivo_path = 'testpdf.pdf'  # Ruta al archivo que deseas adjuntar

    # Enviar el correo
    enviar_con_destinatario(servicio, destinatario, asunto, cuerpo_html_con_firma, imagen_path, archivo_path)

if __name__ == '__main__':
    main()
