from fastapi import FastAPI, HTTPException, Response,status, Depends, APIRouter 
from sqlalchemy.orm import Session
from .. import models, schemas, utils, oauth_2
from ..database import  engine, get_db



router = APIRouter(prefix="/vote", tags=["Vote"])

@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db: Session = Depends(get_db), user_details : schemas.TokenData = Depends(oauth_2.get_current_user)):
    

    post = db.query(models.Posts).filter(models.Posts.id == vote.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {vote.post_id} does not exist")
    
    if not user_details:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="You are not authorized to vote")
    

    vote_query = db.query(models.Votes).filter(models.Votes.post_id == vote.post_id, models.Votes.user_id == user_details.id)
    found_vote = vote_query.first()
    
    if(vote.direction == 1):
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Hii {user_details.name} you have already voted on post {vote.post_id}")
        new_vote = models.Votes(post_id = vote.post_id, user_id = user_details.id) ## set the vote
        db.add(new_vote)
        db.commit()
        return {"message": "Successfully added your vote..."}
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Your vote does not exist on this post")
        vote_query.delete(synchronize_session=False)
        db.commit()

        return {"message": "Successfully deleted the vote"}