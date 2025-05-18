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
    <img src="cid:imagen_cid" alt="Imagen" style="width: 230px; height: auto;" />
    """
    cuerpo_correo = """
    <div style="color: grey; font-family: Verdana, sans-serif;">
        <br>--<br>
        <strong>Patricio Torres Cisternas</strong><br>
        Asistente Soporte y Redes <br>
        +569 6761 2235 <br>
        Avenida Apoquindo 6750 piso 21, Las Condes, RM. <br>
        <a href="www.fundacioncchc.cl">www.fundacioncchc.cl</a> <br>
    </div>
    """
    # Concatenar cuerpo con la firma
    #cuerpo_html_con_firma = cuerpo_html + firma
    cuerpo_html_con_firma = cuerpo_correo + firma
    return cuerpo_html_con_firma