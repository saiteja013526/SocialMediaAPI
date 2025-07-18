from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
from . import schemas
from .config import settings

#SECRET_KEY
#Algorithm
#Expiration time

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes

def create_access_token(data: dict):
    to_encode = data.copy() # Note: we are working on a copy for safety
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        id: str = payload.get("user_id")
        name: str = payload.get("name") # type: ignore

        if id is None or name is None:
            raise credentials_exception

        token_data = schemas.TokenData(id=id, name=name)
        return token_data
    except JWTError:
        raise credentials_exception
    

