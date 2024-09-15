from flask import Flask, render_template
from flask_socketio import SocketIO, send
from services.openai_service import OpenAIService

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)
# Inicializamos el servicio de OpenAI
service = OpenAIService()

# Ruta para el home
@app.route('/')
def index():
    return render_template('index.html')

# Evento de mensaje recibido en el WebSocket
@socketio.on('message')
def handle_message(msg):
    print(f"Mensaje recibido: {msg}")

    response = service.enviar_mensaje(msg)

    send(response, broadcast=True)  # Enviar mensaje a todos los clientes conectados

if __name__ == '__main__':
    socketio.run(app, debug=True)
