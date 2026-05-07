from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from database.DbConnect import get_db
from models import modelDb
from models.models import User, LoginRequest
from security.jwtHandler import create_access_token
from security.securiity import hash_password, verify_password

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post("/register")
def register(user: User, db: Session = Depends(get_db)):

    existing = db.query(modelDb.UserDB).filter(
        modelDb.UserDB.email == user.email
    ).first()

    if existing:
        raise HTTPException(status_code=400, detail="User already exists")

    hashed_pwd = hash_password(user.password)

    u = modelDb.UserDB(
        name=user.name,
        email=user.email,
        password=hashed_pwd
    )

    db.add(u)
    db.commit()
    db.refresh(u)

    return {"message": "User created"}


@router.post("/login")
def login(user: LoginRequest, db: Session = Depends(get_db)):

    db_user = db.query(modelDb.UserDB).filter(
        modelDb.UserDB.email == user.email
    ).first()

    if not db_user or not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=401, detail="Invalid username or password")

    token = create_access_token(user.email)

    return {
        "access_token": token,
        "token_type": "bearer"
    }