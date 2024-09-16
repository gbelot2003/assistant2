import os
from faker import Faker
from flask import Flask, render_template, request, redirect, url_for, session
from flask_socketio import SocketIO, send
from services.openai_service import OpenAIService
from services.conversation_service import ConversationService
import random

app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey!'
socketio = SocketIO(app)

# Configuramos Faker
fake = Faker()

# Inicializamos el servicio de OpenAI
service = OpenAIService()
conversation_service = ConversationService()

# Generamos una lista de usuarios falsos
def generar_usuarios(num_usuarios=10):
    usuarios = []
    for _ in range(num_usuarios):
        usuario = {
            'username': fake.user_name(),
            'password': fake.password()
        }
        usuarios.append(usuario)
    return usuarios

usuarios = generar_usuarios()

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

@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        return render_template('dashboard.html', username=session['username'])
    return redirect(url_for('login'))

# Ruta de login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Verificamos si el usuario existe en nuestra lista de usuarios generados
        for usuario in usuarios:
            if usuario['username'] == username and usuario['password'] == password:
                session['username'] = username
                return redirect(url_for('dashboard'))

        # Si las credenciales no son válidas
        return 'Credenciales inválidas. Intenta nuevamente.'
    return render_template('login.html')

# Ruta de logout
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))


# Evento de mensaje recibido en el WebSocket
@socketio.on('message')
def handle_message(msg):
    conversation_id = None

    # Si el mensaje es un diccionario, extraemos el ID de conversación
    if isinstance(msg, dict) and 'conversation_id' in msg:
        conversation_id = msg['conversation_id']
        user_message = msg['message']
    else:
        user_message = msg

    # Cargamos los archivos automáticamente al inicio
    cargar_archivos_al_iniciar()
    
    print(f"Mensaje recibido: {user_message}")

    response = service.enviar_mensaje(user_message)

    # Guardamos la conversación en la base de datos
    conversation_id = conversation_service.guardar_conversacion(user_message, response, conversation_id)

    print(f"Mensaje Chatgpt: {response}")

    send(response, broadcast=True)  # Enviar mensaje a todos los clientes conectados

if __name__ == '__main__':
    socketio.run(app, debug=True)
