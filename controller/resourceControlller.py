from database.DbConnect import get_db
from fastapi import APIRouter, Depends
from models.modelDb import UserDB, DocumentDB
from models.models import DocumentValidator
from security.dependencies import get_current_user
from service.documentService import addDocument, documentEmbedding
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/user",
    dependencies=[Depends(get_current_user)],
    tags=["Resource"]
)
@router.post("/documet/{chat_id}")
def addocumetfun(udocument:DocumentValidator, chat_id:int,email:str=Depends(get_current_user), db: Session = Depends(get_db)):
    user = db.query(UserDB).filter(UserDB.email == email).first()
    savedoc= addDocument(udocument.fileName,udocument.filePath,chat_id,user.id,db)
    docdb=db.query(DocumentDB).filter(DocumentDB.filePath==udocument.filePath).first()
    documentEmbedding(udocument.filePath,chat_id,user.id,docdb.id)
    return {"message":"Document added successfully"}


@router.get("/documets/{chat_id}")
def get_documet(
        chat_id: int,
        cursor: int = 0,
        limit: int = 20,
        email: str = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    user = db.query(UserDB).filter(
        UserDB.email == email
    ).first()

    documents = (
        db.query(DocumentDB)
        .filter(
            DocumentDB.chat_id == chat_id,
            DocumentDB.user_id == user.id
        )
        .order_by(DocumentDB.id.desc())
        .offset(cursor)
        .limit(limit)
        .all()
    )

    return documents
