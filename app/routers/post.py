from typing import Optional, List
from fastapi import FastAPI, HTTPException, Response,status, Depends,APIRouter
import psycopg2
from sqlalchemy.orm import Session

# from app import oauth_2
from .. import models, schemas, utils, oauth_2
from ..database import  engine, get_db


router = APIRouter(prefix="/posts", tags=["Posts"])



@router.get("/", response_model=List[schemas.PostResponse])
def get_posts(db:Session = Depends(get_db), user_details : schemas.TokenData = Depends(oauth_2.get_current_user)):
    
    posts = db.query(models.Post).all()
    if not posts:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Oops!! There are no posts")
    return posts


@router.get("/{id}", response_model=schemas.PostResponse)
def get_post_by_id(id:int,db:Session = Depends(get_db), user_details : schemas.TokenData = Depends(oauth_2.get_current_user)):

    post_by_id = db.query(models.Post).filter(models.Post.id == id).first()

    if not post_by_id:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} was not found")
    return  post_by_id


@router.post("/createposts", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse, )
def create_a_new_post(post:schemas.PostCreate,db:Session = Depends(get_db), user_details : schemas.TokenData = Depends(oauth_2.get_current_user)):
    
    # print(user_details)
    newly_created_post = models.Post(**post.model_dump())
    db.add(newly_created_post)
    db.commit()
    db.refresh(newly_created_post)

    return newly_created_post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_a_post_by_id(id:int, db:Session = Depends(get_db),user_details : schemas.TokenData = Depends(oauth_2.get_current_user)):
  
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
        
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error while deleting the post"
        )
    

@router.put("/{id}", status_code=status.HTTP_200_OK, response_model=schemas.PostResponse) 
def update_post(id:int, update_post:schemas.PostResponse, db:Session = Depends(get_db),user_details : schemas.TokenData = Depends(oauth_2.get_current_user)):
    try:

        post_query = db.query(models.Post).filter(models.Post.id == id)
        post = post_query.first()

        if post is None:
            raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Post with id {id} not found"
                )
        
        post_query.update(
            {getattr(models.Post, key): value for key, value in update_post.model_dump().items()},
            synchronize_session=False
        )
        db.commit()
        return post_query.first()
    

    except psycopg2.Error as database_error:
        print(f"unexpected error", database_error)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Something went wrong"
        )