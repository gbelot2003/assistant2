from services.openai_service import OpenAIService

# Inicializamos el servicio de OpenAI
service = OpenAIService()

# Función para cargar archivos automáticamente y obtener el contenido
def cargar_archivos_al_iniciar():
    archivos = [
        {"ruta": "Encomiendas_Express-B.pdf", "tipo": "pdf"},   # Cambia las rutas por los archivos reales
        #{"ruta": "ruta/del/archivo2.xlsx", "tipo": "excel"}
    ]
    
    contenido_completo = ""
    
    for archivo in archivos:
        contenido = service.procesar_archivo_y_responder(archivo["ruta"], archivo["tipo"])
        contenido_completo += f"\n{contenido}"  # Concatenamos todo el contenido leído
    
    return contenido_completo

# Función para la consola interactiva
def interactive_console():
    print("Bienvenido a la consola interactiva con OpenAI.")
    print("Cargando archivos y extrayendo información...")

    # Cargamos los archivos automáticamente al inicio
    contenido_archivos = cargar_archivos_al_iniciar()

    print("Archivos cargados correctamente. Puedes comenzar a hacer preguntas.")
    
    while True:
        prompt = input("Tú: ")
        
        if prompt.lower() == 'salir':
            # Llamamos al método de cierre del servicio
            service.cerrar_conversacion(guardar_historial=True)
            break
        
        # Enviamos el mensaje a OpenAI, junto con el contenido de los archivos
        mensaje_completo = f"{contenido_archivos}\n{prompt}"  # Incluimos el contenido del archivo + pregunta del usuario
        response = service.enviar_mensaje(mensaje_completo)
        
        print(f"OpenAI: {response}")

# Punto de entrada del script
if __name__ == "__main__":
    interactive_console()
