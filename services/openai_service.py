import openai
import os
import PyPDF2
import pandas as pd
import chromadb


class OpenAIService:
    def __init__(self):
        # Inicializamos la clave de API desde una variable de entorno
        openai.api_key = os.getenv("OPENAI_API_KEY")
        self.conversation_history = []

        # Inicializamos ChromaDB
        self.chroma_client = chromadb.Client()
        self.collection = self.chroma_client.create_collection("archivo_contenido")


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
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=150,
            )
            # Devolvemos solo la respuesta sin historial
            return response["choices"][0]["message"]["content"]
        except Exception as e:
            return f"Error al comunicarse con OpenAI: {e}"

    def leer_pdf(self, file_path):
        """
        Lee el contenido de un archivo PDF y lo devuelve como texto.
        """
        try:
            with open(file_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                text = ''
                for page_num in range(len(reader.pages)):
                    page = reader.pages[page_num]
                    # Extraemos el texto de cada página y lo limpiamos
                    page_text = page.extract_text()
                    if page_text:
                        text += page_text.strip() + "\n"
            if not text:
                return "Error: No se pudo extraer texto del archivo PDF."
            return text
        except Exception as e:
            return f"Error al leer el archivo PDF: {e}"

    def leer_excel(self, file_path):
        """
        Lee el contenido de un archivo Excel y lo devuelve como texto.
        """
        try:
            df = pd.read_excel(file_path)
            # Convertir el DataFrame a texto de forma sencilla
            text = df.to_string(index=False)
            return text
        except Exception as e:
            return f"Error al leer el archivo Excel: {e}"

    def procesar_archivo_y_guardar_en_chroma(self, file_path, file_type):
        """
        Lee el contenido de un archivo (PDF o Excel) y lo guarda en ChromaDB.
        """
        if file_type == "pdf":
            contenido = self.leer_pdf(file_path)
        elif file_type == "excel":
            contenido = self.leer_excel(file_path)
        else:
            return "Tipo de archivo no soportado."

        if "Error" in contenido:
            return contenido

        # Almacenamos el contenido en ChromaDB
        self.collection.add(
            documents=[contenido],
            metadatas=[{"file_path": file_path, "file_type": file_type}],
            ids=[file_path]  # Usamos la ruta como ID único
        )
        return f"Contenido de {file_path} guardado en ChromaDB."

    def obtener_contenido_desde_chroma(self):
        """
        Recupera todo el contenido guardado en ChromaDB.
        """
        results = self.collection.get()
        contenidos = [doc for doc in results["documents"]]
        return "\n".join(contenidos)

    def procesar_archivo_y_responder(self, file_path, file_type):
        """
        Lee el contenido de un archivo (PDF o Excel), envía el contenido a OpenAI, y devuelve la respuesta.
        """
        if file_type == "pdf":
            contenido = self.leer_pdf(file_path)
        elif file_type == "excel":
            contenido = self.leer_excel(file_path)
        else:
            return "Tipo de archivo no soportado."

        # Enviamos el contenido leído a OpenAI para obtener una respuesta
        if contenido:
            return self.obtener_respuesta(contenido)
        else:
            return "No se pudo obtener contenido del archivo."
