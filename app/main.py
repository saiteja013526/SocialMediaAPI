import time
from typing import Optional
from fastapi import FastAPI, HTTPException, Response,status, Depends
from fastapi.params import Body
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
from sqlalchemy.orm import Session
from . import models
from .database import  engine, get_db


models.Base.metadata.create_all(bind=engine)

app = FastAPI()

class Post(BaseModel):
    title: str
    content: str
    published: bool = True


while True:
    try:
        connection = psycopg2.connect(host='localhost',database='fastapi', user='postgres', password='dell@123' )
        cursor = connection.cursor(cursor_factory=RealDictCursor)
        print("Connected to database successfully!")
        break
    except Exception as error:
        print("connection to Database failed")
        print("error: ",error)
        time.sleep(3)


@app.get("/")
def root():
    return {"message": "This is Sai Teja's API"}

@app.get("/sqlalchemy")
def test_posts(db:Session = Depends(get_db)):

    all_posts = db.query(models.Post).all()
    return all_posts


@app.get("/posts")
def get_posts(db:Session = Depends(get_db)):
    # cursor.execute("""SELECT * FROM posts ORDER BY id """)
    # posts = cursor.fetchall() 
    # return{"data":posts}

    posts = db.query(models.Post).all()
    return posts


@app.get("/posts/{id}")
def get_post_by_id(id:int,db:Session = Depends(get_db)):
    
    # cursor.execute("""SELECT * FROM posts where id = %s """,(str(id),))
    # post_by_id= cursor.fetchone()

    post_by_id = db.query(models.Post).filter(models.Post.id == id).first()

    if not post_by_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} was not found")
    return  post_by_id


@app.post("/createposts", status_code=status.HTTP_201_CREATED)
def create_a_new_post(post:Post,db:Session = Depends(get_db)):
    # cursor.execute("""INSERT INTO posts(title, content, published) values(%s, %s, %s) RETURNING * """,
    #                (post.title, post.content, post.published))   
    # newly_created_post = cursor.fetchone()
    # connection.commit()  

    #newly_created_post = models.Post(title=post.title, content=post.content, published=post.published)
    newly_created_post = models.Post(**post.model_dump())

    db.add(newly_created_post)
    db.commit()

    db.refresh(newly_created_post)
    
    return {newly_created_post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_a_post_by_id(id:int):
  
    try:
        cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(id),))
        deleted_post = cursor.fetchone()
        connection.commit()

        if deleted_post is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Post with id {id} not found"
            )
        return Response(status_code=status.HTTP_204_NO_CONTENT)
    
    
    except psycopg2.Error as db_error:
        print(f"Database error: {db_error}")
        connection.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error while deleting the post"
        )
    

@app.put("/posts/{id}") # 200 status code
def update_post(id:int, post:Post):
    try:
        cursor.execute("""UPDATE posts 
                    set title = %s, content = %s, published =%s WHERE id = %s RETURNING *""",(post.title, post.content, post.published, (str(id)),))
        updated_post = cursor.fetchone()
        connection.commit()
        if updated_post is None:
            return HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Post with id {id} not found"
                )
        return {"data": updated_post}
    

    except psycopg2.Error as database_error:
        print(f"unexpected error", database_error)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Something went wrong"
        )