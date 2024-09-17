from flask_socketio import SocketIO, send
from services.email_service import es_email_valido, enviar_correo  # Importamos las funciones de email_service
from services.file_service import cargar_archivos_al_iniciar  # Importamos la función de carga de archivos

socketio = SocketIO()

def init_socketio(app, service, conversation_service):
    socketio.init_app(app)

    @socketio.on('message')
    def handle_message(msg):
        conversation_id = None
        user_email = None  # Variable para almacenar el correo si se solicita
        
        # Verificar si msg es un diccionario
        if isinstance(msg, dict):
            if 'message' in msg:
                user_message = msg['message']
            if 'email' in msg:
                user_email = msg['email']
        else:
            # Si msg no es un diccionario, se considera un mensaje de texto simple
            user_message = msg

        # Cargar archivos antes de procesar el mensaje
        cargar_archivos_al_iniciar(service)

        # Procesar el mensaje normalmente
        print(f"Mensaje recibido: {user_message}")
        response = service.obtener_respuesta(user_message)

        # Guardar la conversación
        conversation_id = conversation_service.guardar_conversacion(user_message, response, conversation_id)

        send(response, broadcast=True)

    return socketio
