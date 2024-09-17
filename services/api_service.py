# api_service.py

import requests

# Función para manejar solicitudes a una API externa
def manejar_solicitud_api(metodo, url, data=None):
    try:
        if metodo.upper() == "GET":
            response = requests.get(url)
        elif metodo.upper() == "POST":
            response = requests.post(url, json=data)  # Enviar datos en formato JSON
        else:
            return "Método no soportado. Usa GET o POST."

        # Si la solicitud es exitosa
        if response.status_code == 200:
            return response.json()  # Devuelve el contenido JSON de la respuesta
        else:
            return f"Error en la solicitud. Código de estado: {response.status_code}"
    
    except Exception as e:
        return f"Error al realizar la solicitud a la API: {str(e)}"
