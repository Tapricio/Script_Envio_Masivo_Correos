import tkinter as tk
from tkinter import ttk, colorchooser

def obtener_contenido_desde_interfaz():
    resultado = {"mensaje": ""}

    def aplicar_formato(formato):
        texto_seleccionado = text_area.get(tk.SEL_FIRST, tk.SEL_LAST)
        text_area.delete(tk.SEL_FIRST, tk.SEL_LAST)

        estilo = ""

        if formato == "negrita":
            estilo = f"<b>{texto_seleccionado}</b>"
        elif formato == "cursiva":
            estilo = f"<i>{texto_seleccionado}</i>"
        elif formato == "subrayado":
            estilo = f"<u>{texto_seleccionado}</u>"

        text_area.insert(tk.INSERT, estilo)

    def cambiar_color():
        color = colorchooser.askcolor(title="Selecciona un color")[1]
        if color:
            try:
                seleccionado = text_area.get(tk.SEL_FIRST, tk.SEL_LAST)
                text_area.delete(tk.SEL_FIRST, tk.SEL_LAST)
                texto_coloreado = f'<span style="color:{color};">{seleccionado}</span>'
                text_area.insert(tk.INSERT, texto_coloreado)
            except:
                pass

    def cambiar_fuente(event=None):
        fuente = combo_fuente.get()
        try:
            seleccionado = text_area.get(tk.SEL_FIRST, tk.SEL_LAST)
            text_area.delete(tk.SEL_FIRST, tk.SEL_LAST)
            texto_fuente = f'<span style="font-family:{fuente};">{seleccionado}</span>'
            text_area.insert(tk.INSERT, texto_fuente)
        except:
            pass

    def cambiar_tamano(event=None):
        tamano = combo_tamano.get()
        try:
            seleccionado = text_area.get(tk.SEL_FIRST, tk.SEL_LAST)
            text_area.delete(tk.SEL_FIRST, tk.SEL_LAST)
            texto_tamano = f'<span style="font-size:{tamano}px;">{seleccionado}</span>'
            text_area.insert(tk.INSERT, texto_tamano)
        except:
            pass

    def enviar():
        texto = text_area.get("1.0", tk.END).strip()
        texto = texto.replace("\n", "<br>")  # Salto de línea HTML

        firma_html = """<br><br>
        <div style="color: grey; font-family: Verdana, sans-serif;">
            <br>--<br>
            <strong>Patricio Torres Cisternas</strong><br>
            Asistente Soporte y Redes <br>
            +569 6761 2235 <br>
            Avenida Apoquindo 6750 piso 21, Las Condes, RM. <br>
            <a href="https://www.fundacioncchc.cl">www.fundacioncchc.cl</a> <br>
            <img src="cid:imagen_cid" alt="Imagen" style="width: 200px; height: auto;" />

        </div>
        """

        resultado["mensaje"] = f"<div style='font-family: Arial;'>{texto}</div>" + firma_html
        root.destroy()

    # Crear ventana
    root = tk.Tk()
    root.title("Editor de Correo con Formato")

    # Frame de herramientas
    toolbar = tk.Frame(root)
    toolbar.pack(pady=5)

    tk.Button(toolbar, text="Negrita", command=lambda: aplicar_formato("negrita")).pack(side=tk.LEFT, padx=2)
    tk.Button(toolbar, text="Cursiva", command=lambda: aplicar_formato("cursiva")).pack(side=tk.LEFT, padx=2)
    tk.Button(toolbar, text="Subrayado", command=lambda: aplicar_formato("subrayado")).pack(side=tk.LEFT, padx=2)
    tk.Button(toolbar, text="Color", command=cambiar_color).pack(side=tk.LEFT, padx=2)

    # Fuente
    fuentes = ["Arial", "Verdana", "Courier New", "Times New Roman", "Tahoma"]
    combo_fuente = ttk.Combobox(toolbar, values=fuentes, width=15)
    combo_fuente.set("Arial")
    combo_fuente.pack(side=tk.LEFT, padx=2)
    combo_fuente.bind("<<ComboboxSelected>>", cambiar_fuente)

    # Tamaño
    tamanos = [10, 12, 14, 16, 18, 20, 24, 28, 32]
    combo_tamano = ttk.Combobox(toolbar, values=tamanos, width=5)
    combo_tamano.set(14)
    combo_tamano.pack(side=tk.LEFT, padx=2)
    combo_tamano.bind("<<ComboboxSelected>>", cambiar_tamano)

    # Editor
    text_area = tk.Text(root, wrap=tk.WORD, width=100, height=25)
    text_area.pack(pady=10)

    # Botón enviar
    tk.Button(root, text="Aceptar y continuar", command=enviar).pack(pady=5)

    root.mainloop()
    return resultado["mensaje"]
