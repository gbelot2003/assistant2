import openai
import os


class OpenAIService:
    def __init__(self):
        # Inicializamos la clave de API desde una variable de entorno
        openai.api_key = os.getenv("OPENAI_API_KEY")
        self.conversation_history = []

    def enviar_mensaje(self, prompt):
        """
        Envía un mensaje a OpenAI y obtiene la respuesta.
        """
        self.conversation_history.append({"role": "user", "content": prompt})

        try:
            # Llamamos a la API de OpenAI con el historial de la conversación
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=self.conversation_history,
                max_tokens=150,  # Puedes ajustar según la necesidad
            )
            # Procesamos la respuesta y la añadimos al historial
            assistant_message = response["choices"][0]["message"]["content"]
            self.conversation_history.append(
                {"role": "assistant", "content": assistant_message}
            )
            return assistant_message
        except Exception as e:
            return f"Error al comunicarse con OpenAI: {e}"

    def cerrar_conversacion(self, guardar_historial=False):
        """
        Método para cerrar la conversación.
        Puede guardar el historial en un archivo si se especifica.
        """
        print("Cerrando conversación...")

        if guardar_historial:
            with open("historial_conversacion.txt", "w") as file:
                for mensaje in self.conversation_history:
                    rol = mensaje["role"]
                    contenido = mensaje["content"]
                    file.write(f"{rol.capitalize()}: {contenido}\n")
            print("Historial guardado en 'historial_conversacion.txt'.")

        print("La conversación ha finalizado.")

    def obtener_respuesta(self, prompt):
        """
        Método simplificado que envía un mensaje a OpenAI y devuelve solo la respuesta.
        No guarda historial ni realiza acciones adicionales.
        """
        try:
            # Hacemos la llamada a la API de OpenAI con solo el mensaje actual
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=150,
            )
            # Devolvemos solo la respuesta sin historial
            return response["choices"][0]["message"]["content"]
        except Exception as e:
            return f"Error al comunicarse con OpenAI: {e}"
