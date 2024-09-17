# action_service.py

from services.api_service import manejar_solicitud_api
from services.action_url_service import obtener_url_por_accion
from services.file_service import obtener_datos_cargados  # Importar los datos cargados
import re


# Función para procesar el mensaje del usuario
# Función para procesar el mensaje del usuario
def procesar_mensaje(user_message, chatgpt_service):
    # Detectar la acción solicitada en el mensaje del usuario
    accion_detectada = detectar_accion_en_mensaje(user_message)

    if accion_detectada:
        config_url = obtener_url_por_accion(accion_detectada)
        if config_url:
            metodo = config_url["metodo"]
            url = config_url["url"]

            # Obtener datos si es necesario (para solicitudes POST)
            data = (
                obtener_datos_para_accion(accion_detectada, user_message)
                if metodo == "POST"
                else None
            )

            # Verificar si se tienen todos los datos para realizar la acción
            if data and all(data.values()):
                # Enviar solicitud a la URL configurada
                respuesta_api = manejar_solicitud_api(metodo, url, data)
                return f"Respuesta de la API ({metodo}) para {accion_detectada}: {respuesta_api}"
            else:
                # Si faltan datos, avisar al usuario
                return "Parece que falta información en tu solicitud. Por favor, asegúrate de proporcionar el nombre del cliente, producto y precio."
        else:
            return f"No se ha configurado una URL para la acción '{accion_detectada}'"
    else:
        # Si no se detecta ninguna acción, devolver la respuesta normal del ChatGPT
        respuesta_chatgpt = chatgpt_service.enviar_mensaje(user_message)

        # Incluir datos cargados en las respuestas si son relevantes
        datos_cargados = obtener_datos_cargados()
        if "precios" in user_message.lower() or "encomiendas" in user_message.lower():
            if datos_cargados:
                respuesta_chatgpt += "\n\nInformación disponible sobre encomiendas:\n"
                for archivo, datos in datos_cargados.items():
                    respuesta_chatgpt += f"Archivo: {archivo} - Datos: {datos}\n"
            else:
                respuesta_chatgpt += (
                    "\nNo se han encontrado datos cargados sobre encomiendas."
                )

        return respuesta_chatgpt


# Función para detectar la acción solicitada en el mensaje
def detectar_accion_en_mensaje(mensaje):
    acciones_configuradas = ["enviar cotización", "consultar precios"]
    for accion in acciones_configuradas:
        if accion in mensaje.lower():
            return accion
    return None


# Función para obtener los datos necesarios para una solicitud POST
def obtener_datos_para_accion(accion, user_message):
    # Inicializamos un diccionario para almacenar los datos extraídos
    datos = {}

    # Buscamos el nombre del cliente (Ejemplo: "cliente Juan Pérez")
    cliente_match = re.search(r"cliente\s(\w+\s\w+)", user_message.lower())
    if cliente_match:
        datos["cliente"] = cliente_match.group(1).title()  # Extraemos y capitalizamos el nombre
    
    # Buscamos el producto solicitado (Ejemplo: "producto Servicio X")
    producto_match = re.search(r"producto\s([\w\s]+)", user_message.lower())
    if producto_match:
        datos["producto"] = producto_match.group(1).strip().title()  # Extraemos y capitalizamos el producto

    # Buscamos un precio en el mensaje (Ejemplo: "precio 150" o "costo 150")
    precio_match = re.search(r"(precio|costo)\s(\d+)", user_message.lower())
    if precio_match:
        datos["precio"] = int(precio_match.group(2))  # Extraemos el precio como entero

    # Valores predeterminados en caso de que no se encuentren coincidencias
    if "cliente" not in datos:
        datos["cliente"] = None
    if "producto" not in datos:
        datos["producto"] = None
    if "precio" not in datos:
        datos["precio"] = None

    return datos
