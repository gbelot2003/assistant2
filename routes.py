# routes.py
from flask import render_template
from flask_socketio import send
from services.openai_service import OpenAIService
from services.conversation_service import ConversationService
from services.socket_service import init_socketio

# Crear las instancias de los servicios
service = OpenAIService()
conversation_service = ConversationService()

def configure_routes(app, socketio):
    # Ruta para el home
    @app.route("/")
    def index():
        return render_template("index.html")

    # Inicializar socketio con los servicios
    socketio = init_socketio(app, service, conversation_service)
