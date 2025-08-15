from fastapi import FastAPI
from . import models
from .database import  engine
from .routers import post, user, auth, votes
from .config import settings


print(f"Loading settings for database: {settings.database_name}")

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(votes.router)






    

