# action_url_service.py

# Configuración de URLs para diferentes acciones
ACCIONES_URLS = {
    "enviar cotización": {
        "metodo": "POST",
        "url": "https://webhook.site/da11f8eb-7965-4c07-921d-419732540da6"
    },
    "consultar precios": {
        "metodo": "GET",
        "url": "https://api.example.com/consultar_precios"
    }
    # Puedes agregar más acciones aquí
}

# Función para obtener la URL y método basado en la acción solicitada
def obtener_url_por_accion(accion):
    accion = accion.lower()
    if accion in ACCIONES_URLS:
        return ACCIONES_URLS[accion]
    else:
        return None
