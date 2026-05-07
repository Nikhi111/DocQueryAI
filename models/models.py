from pydantic import BaseModel, EmailStr


class User(BaseModel) :

    name:str
    email:str
    password:str
class Chat(BaseModel) :

    name:str
    description:str

class LoginRequest(BaseModel):
    email: EmailStr
    password: str