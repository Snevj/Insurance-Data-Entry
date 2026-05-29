# models/db_models.py
from sqlalchemy import create_engine, Column, Integer, String, Text, DateTime
from sqlalchemy.orm import declarative_base, sessionmaker
from datetime import datetime
from config import DATABASE_URL

Base = declarative_base()
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)

class ChatMessage(Base):
    __tablename__ = "chat_messages"
    id = Column(Integer, primary_key=True)
    role = Column(String(10))        # 'user' or 'assistant'
    content = Column(Text)
    timestamp = Column(DateTime, default=datetime.utcnow)

class ExtractedData(Base):
    __tablename__ = "extracted_data"
    id = Column(Integer, primary_key=True)
    filename = Column(String(255))
    policy_number = Column(String(100))
    claimant_name = Column(String(255))
    date = Column(String(100))
    raw_text = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

Base.metadata.create_all(engine)