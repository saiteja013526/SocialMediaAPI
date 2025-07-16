from typing import Optional, List
from fastapi import FastAPI, HTTPException, Response,status, Depends
import psycopg2
from sqlalchemy.orm import Session
from . import models, schemas, utils
from .database import connection, engine, get_db, connection
from .routers import post, user




models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(post.router)
app.include_router(user.router)






    

