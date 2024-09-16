from flask import Flask, render_template
from flask_socketio import SocketIO, send
from services.openai_service import OpenAIService
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)
# Inicializamos el servicio de OpenAI
service = OpenAIService()


# Función para cargar archivos automáticamente y guardarlos en ChromaDB
def cargar_archivos_al_iniciar():
    archivos = [
        {"ruta": "files/Encomiendas_Express-B.pdf", "tipo": "pdf"},   # Cambia las rutas por los archivos reales
    ]
    
    for archivo in archivos:
        ruta = archivo["ruta"]
        tipo = archivo["tipo"]

        # Verificamos si el archivo existe
        if not os.path.exists(ruta):
            print(f"Error: El archivo {ruta} no se encontró.")
            continue  # Pasamos al siguiente archivo si no existe

        # Guardamos el contenido en ChromaDB
        resultado = service.procesar_archivo_y_guardar_en_chroma(ruta, tipo)
        print(resultado)

# Ruta para el home
@app.route('/')
def index():
    return render_template('index.html')

# Evento de mensaje recibido en el WebSocket
@socketio.on('message')
def handle_message(msg):
    # Cargamos los archivos automáticamente al inicio
    cargar_archivos_al_iniciar()
    
    print(f"Mensaje recibido: {msg}")

    response = service.enviar_mensaje(msg)

    send(response, broadcast=True)  # Enviar mensaje a todos los clientes conectados

if __name__ == '__main__':
    socketio.run(app, debug=True)
