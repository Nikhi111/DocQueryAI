from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from service.chatService import saveMessage, getLlmResult
from sqlalchemy.orm import Session

from database.DbConnect import get_db
from models.modelDb import UserDB, ChatDB, MessageDB
from models.models import Chat, Message
from security.dependencies import get_current_user

router = APIRouter(
    prefix="/user",
    dependencies=[Depends(get_current_user)],
    tags=["Chat"]
)

@router.get("/greet")
def greet_user(user=Depends(get_current_user)):
    return f"welcome {user}"

@router.post("/create")
def createChat(
    chat: Chat,
    email: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    userdb = db.query(UserDB).filter(UserDB.email == email).first()

    c = ChatDB(
        name=chat.name,
        description=chat.description,
        user_id=userdb.id
    )

    db.add(c)
    db.commit()
    db.refresh(c)

    return c;


@router.put("/{chat_id}/{name}")
def renameChat(
    chat_id: int,
    name: str,
    email: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    userdb = db.query(UserDB).filter(UserDB.email == email).first()

    chat = db.query(ChatDB).filter(ChatDB.id == chat_id).first()

    if chat is None:
        raise HTTPException(status_code=404, detail="Chat not found")

    chat.name = name
    db.commit()
    db.refresh(chat)

    return "chat renamed"


@router.get("/chats")
def getChats(
    email: str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    user = db.query(UserDB).filter(UserDB.email == email).first()
    chats = db.query(ChatDB).filter(ChatDB.user_id == user.id).all()

    return chats
@router.post("/chat/{chat_id}/message")
def addMessage(message:str,chat_id: int, email: str = Depends(get_current_user),db: Session = Depends(get_db)):
    user = db.query(UserDB).filter(UserDB.email == email).first()
    savedMessage=saveMessage(message,"User",user.id,chat_id,db)
    agnetResponse=getLlmResult(message,user.id,chat_id)
    agentMessage=saveMessage(agnetResponse.content,"Agent",user.id,chat_id,db)
    return  {
    "id": agentMessage.id,
    "content": agentMessage.content,
    "role": agentMessage.role,
    "created_at": agentMessage.created_at
}
@router.get("/chat/messages")
def get_messages(
    chat_id: int,
    cursor: Optional[int] = None,
    limit: int = Query(20, le=50),
    email:str = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    query = db.query(MessageDB)\
              .filter(MessageDB.chat_id == chat_id)\
              .order_by(MessageDB.id.desc())

    # Apply cursor
    if cursor:
        query = query.filter(MessageDB.id < cursor)

    messages = query.limit(limit).all()

    # Convert to ascending for UI
    messages.reverse()

    return {
        "data": messages,
        "next_cursor": messages[0].id if messages else None,
        "has_more": len(messages) == limit
    }


