from datetime import datetime, timedelta
from jose import jwt

from config import SECRET_KEY, ALGORITHM


def create_access_token(email:str ):
    expire = datetime.utcnow() + timedelta(minutes=30)

    payload = {
        "sub": email,
        "exp": expire
    }

    return jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)