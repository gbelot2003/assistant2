from services.openai_service import OpenAIService

# Inicializamos el servicio de OpenAI
service = OpenAIService()

# Función para la consola interactiva
def interactive_console():
    print("Bienvenido a la consola interactiva con OpenAI. Escribe 'salir' para terminar la conversación.")
    
    while True:
        prompt = input("Tú: ")
        
        if prompt.lower() == 'salir':
            # Llamamos al método de cierre del servicio
            service.cerrar_conversacion(guardar_historial=True)
            break
        
        # Enviamos el mensaje a OpenAI y mostramos la respuesta
        response = service.enviar_mensaje(prompt)
        print(f"OpenAI: {response}")

# Punto de entrada del script
if __name__ == "__main__":
    interactive_console()