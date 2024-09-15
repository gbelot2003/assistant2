import os
from services.openai_service import OpenAIService

# Inicializamos el servicio de OpenAI
service = OpenAIService()

# Función para cargar archivos automáticamente y guardarlos en ChromaDB
def cargar_archivos_al_iniciar():
    archivos = [
        {"ruta": "files/Encomiendas_Express-B.pdf", "tipo": "pdf"},   # Cambia las rutas por los archivos reales
    ]
    
    for archivo in archivos:
        ruta = archivo["ruta"]
        tipo = archivo["tipo"]

        # Verificamos si el archivo existe
        if not os.path.exists(ruta):
            print(f"Error: El archivo {ruta} no se encontró.")
            continue  # Pasamos al siguiente archivo si no existe

        # Guardamos el contenido en ChromaDB
        resultado = service.procesar_archivo_y_guardar_en_chroma(ruta, tipo)
        print(resultado)

# Función para la consola interactiva
def interactive_console():
    print("Bienvenido a la consola interactiva con OpenAI.")
    print("Cargando archivos y guardando la información en la base de datos...")

    # Cargamos los archivos automáticamente al inicio
    cargar_archivos_al_iniciar()

    print("Archivos cargados correctamente. Puedes comenzar a hacer preguntas.")
    
    while True:
        prompt = input("Tú: ")
        
        if prompt.lower() == 'salir':
            # Llamamos al método de cierre del servicio
            service.cerrar_conversacion(guardar_historial=True)
            break
        
        # Recuperamos el contenido almacenado en ChromaDB
        contenido_archivos = service.obtener_contenido_desde_chroma()

        # Enviamos el mensaje a OpenAI, junto con el contenido de los archivos
        mensaje_completo = f"{contenido_archivos}\n{prompt}"  # Incluimos el contenido del archivo + pregunta del usuario
        response = service.enviar_mensaje(mensaje_completo)
        
        print(f"OpenAI: {response}")

# Punto de entrada del script
if __name__ == "__main__":
    interactive_console()
