import os
from faker import Faker
from flask import Flask, render_template, request, redirect, url_for, session
from flask_socketio import SocketIO, send
from services.socket_service import init_socketio
from services.openai_service import OpenAIService
from services.conversation_service import ConversationService

app = Flask(__name__)
app.config["SECRET_KEY"] = "supersecretkey!"
socketio = SocketIO(app)

# Inicializamos el servicio de OpenAI
service = OpenAIService()
conversation_service = ConversationService()

# Initialize SocketIO
socketio = init_socketio(app, service, conversation_service)

# Ruta para el home
@app.route("/")
def index():
    return render_template("index.html")


if __name__ == "__main__":
    socketio.run(app, debug=True)
