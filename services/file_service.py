# file_service.py

import os
import json

ARCHIVO_REGISTRO = 'cargados.json'
datos_cargados = {}  # Variable global para almacenar los datos cargados

# Función para cargar archivos solo si no han sido procesados previamente
def cargar_archivos_al_iniciar(service):
    global datos_cargados  # Asegurarse de que estamos usando la variable global
    archivos = [
        {"ruta": "files/Encomiendas_Express-B.pdf", "tipo": "pdf"},  # Añade más archivos si es necesario
    ]

    archivos_cargados = cargar_archivos_cargados()

    for archivo in archivos:
        ruta = archivo["ruta"]
        tipo = archivo["tipo"]

        if ruta in archivos_cargados:
            print(f"El archivo {ruta} ya ha sido procesado previamente. Saltando...")
            continue

        if not os.path.exists(ruta):
            print(f"Error: El archivo {ruta} no se encontró.")
            continue

        try:
            resultado = service.procesar_archivo_y_guardar_en_chroma(ruta, tipo)
            print(f"Archivo {ruta} procesado correctamente: {resultado}")

            archivos_cargados[ruta] = True
            guardar_archivos_cargados(archivos_cargados)

            # Guardamos los datos procesados en la variable global
            datos_cargados[ruta] = resultado  # Los datos cargados se almacenan aquí
        except Exception as e:
            print(f"Error al procesar el archivo {ruta}: {str(e)}")

# Función para obtener los datos cargados
def obtener_datos_cargados():
    global datos_cargados
    return datos_cargados


# Función para cargar los archivos ya procesados desde un archivo JSON
def cargar_archivos_cargados():
    if not os.path.exists(ARCHIVO_REGISTRO):
        return {}

    with open(ARCHIVO_REGISTRO, 'r') as file:
        try:
            return json.load(file)
        except json.JSONDecodeError:
            return {}

# Función para guardar el estado de los archivos procesados en un archivo JSON
def guardar_archivos_cargados(archivos_cargados):
    with open(ARCHIVO_REGISTRO, 'w') as file:
        json.dump(archivos_cargados, file, indent=4)