# app.py
from flask import Flask
from flask_socketio import SocketIO
from routes import configure_routes  # Importamos las rutas

app = Flask(__name__)
app.config["SECRET_KEY"] = "supersecretkey!"
socketio = SocketIO(app)

# Configurar las rutas
configure_routes(app, socketio)

if __name__ == "__main__":
    socketio.run(app, debug=True)