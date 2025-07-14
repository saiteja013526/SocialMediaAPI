from typing import Optional, List
from fastapi import FastAPI, HTTPException, Response,status, Depends
import psycopg2
from sqlalchemy.orm import Session
from . import models, schemas, utils
from .database import connection, engine, get_db, connection



models.Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/")
def root():
    return {"message": "This is Sai Teja's API"}


@app.get("/posts", response_model=List[schemas.PostResponse])
def get_posts(db:Session = Depends(get_db)):
    
    posts = db.query(models.Post).all()
    if not posts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Oops!! There are no posts")
    return posts


@app.get("/posts/{id}", response_model=schemas.PostResponse)
def get_post_by_id(id:int,db:Session = Depends(get_db)):

    post_by_id = db.query(models.Post).filter(models.Post.id == id).first()

    if not post_by_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} was not found")
    return  post_by_id


@app.post("/posts/createposts", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_a_new_post(post:schemas.PostCreate,db:Session = Depends(get_db)):
    
    newly_created_post = models.Post(**post.model_dump())
    db.add(newly_created_post)
    db.commit()
    db.refresh(newly_created_post)

    return newly_created_post


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_a_post_by_id(id:int, db:Session = Depends(get_db)):
  
    try:
        
        post_query = db.query(models.Post).filter(models.Post.id == id)
        post = post_query.first()

        if post is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Post with id {id} not found"
            )
        
        post_query.delete(synchronize_session=False)
        db.commit()
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    
    
    except psycopg2.Error as db_error:
        print(f"Database error: {db_error}")
        connection.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error while deleting the post"
        )
    

@app.put("/posts/{id}", status_code=status.HTTP_200_OK, response_model=schemas.PostResponse) 
def update_post(id:int, update_post:schemas.PostResponse, db:Session = Depends(get_db)):
    try:

        post_query = db.query(models.Post).filter(models.Post.id == id)
        post = post_query.first()

        if post is None:
            return HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Post with id {id} not found"
                )
        
        post_query.update(update_post.model_dump(), synchronize_session=False)
        db.commit()
        # db.refresh(post)
        return post_query.first()
    

    except psycopg2.Error as database_error:
        print(f"unexpected error", database_error)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Something went wrong"
        )
    


@app.post("/users/create", status_code=status.HTTP_201_CREATED,response_model=schemas.UserResponse )
def create_a_new_user(user: schemas.UserCreate,db:Session = Depends(get_db)):
    
    hashed_password = utils.hash(user.password)
    user.password = hashed_password

    newly_created_user = models.Users(**user.model_dump())
    db.add(newly_created_user)
    db.commit()
    db.refresh(newly_created_user)
    return newly_created_user


@app.get("/users/{id}", response_model=schemas.UserResponse)
def get_user_by_id(id:int,db:Session = Depends(get_db)):

    user = db.query(models.Users).filter(models.Users.id == id).first()

    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} was not found")
    return  user
