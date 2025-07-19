from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
from fastapi import FastAPI, HTTPException, Response,status, Depends, APIRouter
from fastapi.security import OAuth2PasswordBearer
from . import schemas
from .config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

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
        id: int = payload.get("user_id") # type: ignore
        name: str = payload.get("name") # type: ignore

        if id is None or name is None:
            raise credentials_exception

        token_data = schemas.TokenData(id=id, name=name)
        return token_data
    except JWTError as e:
        print(f"JWTError: {e}")
        raise credentials_exception
    except Exception as e:
        print(f"Unexpected error: {e}")
        raise credentials_exception



def get_current_user(token:str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(status_code = status.HTTP_403_FORBIDDEN, detail=f"Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})
    return verify_access_token(token, credentials_exception)