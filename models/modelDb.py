from datetime import datetime
from database.DbConnect import Base
from sqlalchemy import Column, Integer, String, ForeignKey,DateTime
from sqlalchemy.orm import relationship


class UserDB(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password = Column(String, nullable=False)

    # One-to-Many
    chats = relationship("ChatDB", back_populates="user", cascade="all, delete")
class ChatDB(Base):
    __tablename__ = "chats"

    id = Column(Integer, primary_key=True)
    name = Column(String)
    description = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))
    user = relationship("UserDB", back_populates="chats")
    messages = relationship("MessageDB", back_populates="chat", cascade="all, delete")
    documents=relationship("DocumentDB", back_populates="chat", cascade="all, delete")
class DocumentDB(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    fileName = Column(String, nullable=False)
    filePath = Column(String, nullable=False)

    user_id = Column(Integer, ForeignKey("users.id"))
    chat_id = Column(Integer, ForeignKey("chats.id"))

    chat = relationship("ChatDB", back_populates="documents")  # ✅ FIX
class MessageDB(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(String, nullable=False)
    role = Column(String, nullable=False)

    chat_id = Column(Integer, ForeignKey("chats.id"))
    user_id = Column(Integer, ForeignKey("users.id"))

    created_at = Column(DateTime, default=datetime.utcnow)

    chat = relationship("ChatDB", back_populates="messages")  # ✅ FIX
    user = relationship("UserDB")  # optional