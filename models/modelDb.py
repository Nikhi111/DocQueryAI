from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from DbConnect import Base

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