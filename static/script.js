// Conexión con el servidor WebSocket
var socket = io();

// Al hacer clic en el botón enviar
document.getElementById('send-btn').addEventListener('click', function() {
    let message = document.getElementById('message').value;
    if (message) {
        socket.send(message);  // Enviar el mensaje al servidor
        document.getElementById('message').value = '';  // Limpiar el campo
    }
});

// Escuchar mensajes desde el servidor
socket.on('message', function(msg) {
    let chatBox = document.getElementById('chat-box');
    let messageElement = document.createElement('div');
    messageElement.textContent = msg;
    chatBox.appendChild(messageElement);
    chatBox.scrollTop = chatBox.scrollHeight;  // Scroll automático
});
