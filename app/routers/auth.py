from fastapi import FastAPI, HTTPException, Response,status, Depends, APIRouter
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
import psycopg2
from sqlalchemy.orm import Session
from .. import models, schemas, utils, oauth_2
from ..import database 


router = APIRouter(tags=["Authentication"])


@router.post("/login")
# def login(user_credentials: schemas.UserLogin, db:Session = Depends(database.get_db)):    --->> this works fine but
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db:Session = Depends(database.get_db)): #OAuth2PasswordRequestForm--> no longer send the data for this reqyest in body. instead use the form data.

    #user = db.query(models.Users).filter(models.Users.email == user_credentials.email).first()
    # {
    #     "username": user_credentials.username,
    #     "password": user_credentials.password   this is how OAuth2PasswordRequestForm takes data but here username is email
    # }
    user = db.query(models.Users).filter(models.Users.email == user_credentials.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")
    
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")
    
    # create a token and return it
    access_token = oauth_2.create_access_token(data={"user_id": user.id, "name": user.name})

    return {"token": access_token, "token_type": "bearer"}