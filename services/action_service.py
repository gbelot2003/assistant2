# action_service.py

from services.api_service import manejar_solicitud_api
from services.action_url_service import obtener_url_por_accion
from services.file_service import obtener_datos_cargados  # Importar los datos cargados

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
            data = obtener_data_del_mensaje(user_message) if metodo == "POST" else None

            # Enviar solicitud a la URL configurada
            respuesta_api = manejar_solicitud_api(metodo, url, data)
            return f"Respuesta de la API ({metodo}) para {accion_detectada}: {respuesta_api}"
        else:
            return f"No se ha configurado una URL para la acción '{accion_detectada}'"
    else:
        # Si no se detecta ninguna acción, devolver la respuesta normal del ChatGPT
        respuesta_chatgpt = chatgpt_service.obtener_respuesta(user_message)

        # Incluir datos cargados en las respuestas si son relevantes
        datos_cargados = obtener_datos_cargados()
        if "precios" in user_message.lower() or "encomiendas" in user_message.lower():
            if datos_cargados:
                respuesta_chatgpt += "\n\nInformación disponible sobre encomiendas:\n"
                for archivo, datos in datos_cargados.items():
                    respuesta_chatgpt += f"Archivo: {archivo} - Datos: {datos}\n"
            else:
                respuesta_chatgpt += "\nNo se han encontrado datos cargados sobre encomiendas."

        return respuesta_chatgpt

# Función para detectar la acción solicitada en el mensaje
def detectar_accion_en_mensaje(mensaje):
    acciones_configuradas = ["enviar cotización", "consultar precios"]
    for accion in acciones_configuradas:
        if accion in mensaje.lower():
            return accion
    return None

# Función para extraer los datos del mensaje en caso de ser POST
def obtener_data_del_mensaje(mensaje):
    return {"ejemplo_clave": "ejemplo_valor"}  # Datos de ejemplo
