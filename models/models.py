# models.py
from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Conversation(Base):
    __tablename__ = 'conversations'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    conversation_id = Column(String, unique=True, nullable=False)
    user_message = Column(String, nullable=False)
    response = Column(String, nullable=False)

# Configuración de la base de datos SQLite
engine = create_engine('sqlite:///database.sqlite')
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()
