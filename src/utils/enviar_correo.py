# Función para enviar el correo
import base64
from email import encoders
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os


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
