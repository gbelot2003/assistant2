# services/socket_service.py
import os
import smtplib
from email.mime.text import MIMEText
from flask_socketio import SocketIO, send

socketio = SocketIO()


def init_socketio(app, service, conversation_service):
    socketio.init_app(app)

    @socketio.on("message")
    def handle_message(msg):
        conversation_id = None
        enviar_correo_flag = False  # Flag para saber si se debe enviar un correo
        user_email = None  # Variable para almacenar el correo del usuario

        if isinstance(msg, dict):
            if "conversation_id" in msg:
                conversation_id = msg["conversation_id"]
            if "email" or "correo" in msg:
                enviar_correo_flag = True
                user_email = msg[
                    "email"
                ]  # Extraer el correo del usuario si se proporciona
            user_message = msg["message"]
        else:
            user_message = msg

        # Cargar archivos antes de procesar el mensaje
        cargar_archivos_al_iniciar(service)

        print(f"Mensaje recibido: {user_message}")
        response = service.obtener_respuesta(user_message)

        # Guardar la conversación
        conversation_id = conversation_service.guardar_conversacion(
            user_message, response, conversation_id
        )
        print(f"Mensaje ChatGPT: {response}")

                # Enviar correo si el usuario lo solicitó
        if enviar_correo_flag and user_email:
            enviar_correo(user_email, user_message, response)

        send(response, broadcast=True)  # Envía a todos los clientes conectados

    return socketio


def cargar_archivos_al_iniciar(service):
    archivos = [
        {"ruta": "files/Encomiendas_Express-B.pdf", "tipo": "pdf"},
    ]
    for archivo in archivos:
        ruta = archivo["ruta"]
        tipo = archivo["tipo"]
        if not os.path.exists(ruta):
            print(f"Error: El archivo {ruta} no se encontró.")
            continue
        resultado = service.procesar_archivo_y_guardar_en_chroma(ruta, tipo)
        print(resultado)


# Función para enviar correo electrónico
def enviar_correo(destinatario, asunto, mensaje):
    remitente = "gbelot2003@hotmail.com"  # Cambia esto por tu correo
    password = os.getenv("MS_PASSWORD")  # Cambia esto por tu contraseña

    # Configurar el mensaje
    msg = MIMEText(mensaje)
    msg['Subject'] = f"Información solicitada: {asunto}"
    msg['From'] = remitente
    msg['To'] = destinatario

    # Enviar el correo
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(remitente, password)
        server.sendmail(remitente, destinatario, msg.as_string())
        server.quit()
        print(f"Correo enviado a {destinatario}")
    except Exception as e:
        print(f"Error al enviar correo: {str(e)}")
