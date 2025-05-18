from src.utils.enviar_correo import enviar_con_destinatario
from src.utils.autenticacion import obtener_servicio
from src.utils.contenido_correo import generar_contenido_html
import time
from correos_prueba import destinos
from src.utils.interfaz_editor import obtener_contenido_desde_interfaz


#destinos = destinos
destinos = "patriciotcisternas95@gmail.com"


def main():
    servicio = obtener_servicio()
    asunto = "Correo de prueba con firma, imagen y archivo adjunto"
    #cuerpo_html_con_firma = generar_contenido_html()
    cuerpo_html_con_firma = obtener_contenido_desde_interfaz()
    imagen_path = 'img.png'
    archivo_path = 'testpdf.pdf'
    correos_buenos =0
    correos_malos =0
    inicio = time.perf_counter()
    if isinstance(destinos, str):
        try:
            enviar_con_destinatario(servicio, destinos, asunto, cuerpo_html_con_firma, imagen_path, archivo_path)    
            correos_buenos+=1
        except Exception as e:
            print(str(e))
            correos_malos+=1
        
    else:
        for d in destinos:
            try:
                enviar_con_destinatario(servicio, d, asunto, cuerpo_html_con_firma, imagen_path, archivo_path)
                correos_buenos+=1
            except Exception as e:
                print(str(e))
                correos_malos+=1
                continue
        
                
    fin = time.perf_counter()
    duracion = fin - inicio
    print(f"\n✅ Tiempo total de envío: {duracion:.2f} segundos.")
    print(f"correos buenos {correos_buenos}")
    print(f"correos malos {correos_malos}")

if __name__ == '__main__':
    main()
