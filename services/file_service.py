import os
import json

# Ruta del archivo de registro
ARCHIVO_REGISTRO = "cargados.json"


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
