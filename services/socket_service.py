from flask_socketio import SocketIO, send
from services.file_service import cargar_archivos_al_iniciar
from services.action_service import procesar_mensaje  # Importar la lógica de acciones

socketio = SocketIO()

def init_socketio(app, service, conversation_service):
    socketio.init_app(app)

    # Cargar archivos al iniciar la aplicación (una vez)
    cargar_archivos_al_iniciar(service)

    @socketio.on("message")
    def handle_message(msg):
        conversation_id = None
        user_message = None

        # Verificar si msg es un diccionario
        if isinstance(msg, dict):
            if 'message' in msg:
                user_message = msg['message']
        else:
            user_message = msg

        # Procesar el mensaje a través del action_service y ChatGPT
        response = procesar_mensaje(user_message, service)

        # Guardar la conversación
        conversation_id = conversation_service.guardar_conversacion(user_message, response, conversation_id)

        send(response, broadcast=True)

    return socketio
