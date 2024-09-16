# services/conversation_service.py
from models.models import Conversation, session
import uuid

class ConversationService:
    def generar_id_conversacion(self):
        """Genera un ID único para la conversación."""
        return str(uuid.uuid4())

    def guardar_conversacion(self, user_message, response, conversation_id=None):
        """Guarda la conversación en la base de datos."""
        if not conversation_id:
            conversation_id = self.generar_id_conversacion()

        nueva_conversacion = Conversation(
            conversation_id=conversation_id,
            user_message=user_message,
            response=response
        )
        session.add(nueva_conversacion)
        session.commit()

        return conversation_id

    def obtener_conversacion(self, conversation_id):
        """Recupera una conversación por su ID."""
        return session.query(Conversation).filter_by(conversation_id=conversation_id).all()
