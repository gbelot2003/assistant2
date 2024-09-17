# email_service.py
import re
import smtplib
from email.mime.text import MIMEText


# Función para validar si un correo es válido
def es_email_valido(email):
    regex = r"^\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
    return re.match(regex, email)


# Función para enviar correos electrónicos
def enviar_correo(destinatario, asunto, mensaje):
    remitente = "tu_correo@gmail.com"  # Cambia esto por tu correo
    password = "tu_contraseña"  # Cambia esto por tu contraseña

    # Configurar el mensaje
    msg = MIMEText(mensaje)
    msg["Subject"] = asunto
    msg["From"] = remitente
    msg["To"] = destinatario

    # Enviar el correo
    try:
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(remitente, password)
        server.sendmail(remitente, destinatario, msg.as_string())
        server.quit()
        print(f"Correo enviado a {destinatario}")
    except Exception as e:
        print(f"Error al enviar correo: {str(e)}")
