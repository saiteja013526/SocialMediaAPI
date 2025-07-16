from typing import Optional, List
from fastapi import FastAPI, HTTPException, Response,status, Depends, APIRouter
import psycopg2
from sqlalchemy.orm import Session
from .. import models, schemas, utils
from ..database import connection, engine, get_db, connection


router = APIRouter(prefix="/users", tags=["Users"])



@router.post("/create", status_code=status.HTTP_201_CREATED,response_model=schemas.UserResponse )
def create_a_new_user(user: schemas.UserCreate,db:Session = Depends(get_db)):
    
    hashed_password = utils.hash(user.password)
    user.password = hashed_password

    newly_created_user = models.Users(**user.model_dump())
    db.add(newly_created_user)
    db.commit()
    db.refresh(newly_created_user)
    return newly_created_user


@router.get("/{id}", response_model=schemas.UserResponse)
def get_user_by_id(id:int,db:Session = Depends(get_db)):

    user = db.query(models.Users).filter(models.Users.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id: {id} was not found")
    return  user
