# services/socket_service.py
import os
import json
from email.mime.text import MIMEText
from flask_socketio import SocketIO, send
from services.email_service import (
    es_email_valido,
    enviar_correo,
)  # Importamos las funciones de email_service

socketio = SocketIO()

# Ruta del archivo de registro
ARCHIVO_REGISTRO = "cargados.json"


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


# Función para cargar archivos solo si no han sido procesados previamente
def cargar_archivos_al_iniciar(service):
    archivos = [
        {
            "ruta": "files/Encomiendas_Express-B.pdf",
            "tipo": "pdf",
        },  # Añade más archivos según sea necesario
    ]

    # Leer el archivo de registro de archivos cargados
    archivos_cargados = cargar_archivos_cargados()

    for archivo in archivos:
        ruta = archivo["ruta"]
        tipo = archivo["tipo"]

        # Verificar si el archivo ya ha sido procesado
        if ruta in archivos_cargados:
            print(f"El archivo {ruta} ya ha sido procesado previamente. Saltando...")
            continue  # Saltamos este archivo si ya ha sido cargado

        # Verificamos si el archivo existe
        if not os.path.exists(ruta):
            print(f"Error: El archivo {ruta} no se encontró.")
            continue  # Pasamos al siguiente archivo si no existe

        # Procesamos el archivo y lo guardamos en la base de datos (ChromaDB, etc.)
        try:
            resultado = service.procesar_archivo_y_guardar_en_chroma(ruta, tipo)
            print(f"Archivo {ruta} procesado correctamente: {resultado}")

            # Añadimos el archivo al registro de archivos cargados
            archivos_cargados[ruta] = True
            guardar_archivos_cargados(archivos_cargados)
        except Exception as e:
            print(f"Error al procesar el archivo {ruta}: {str(e)}")


# Función para cargar los archivos ya procesados desde un archivo JSON
def cargar_archivos_cargados():
    if not os.path.exists(ARCHIVO_REGISTRO):
        return {}

    with open(ARCHIVO_REGISTRO, "r") as file:
        try:
            return json.load(file)
        except json.JSONDecodeError:
            return {}


# Función para guardar el estado de los archivos procesados en un archivo JSON
def guardar_archivos_cargados(archivos_cargados):
    with open(ARCHIVO_REGISTRO, "w") as file:
        json.dump(archivos_cargados, file, indent=4)
