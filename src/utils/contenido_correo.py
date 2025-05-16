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