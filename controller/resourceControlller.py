from database.DbConnect import get_db
from fastapi import APIRouter, Depends
from models.models import DocumentValidator
from security.dependencies import get_current_user
from service.documentService import addDocument
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/user",
    dependencies=[Depends(get_current_user)],
    tags=["Resouce"]
)
@router.post("/documet")
def addocumetfun(udocument:DocumentValidator,email:str=Depends(get_current_user), db: Session = Depends(get_db)):
    addDocument(udocument,email,db)
    return {"message":"Document added successfully"}
