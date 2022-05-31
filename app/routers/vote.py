from fastapi import Depends, FastAPI, status, HTTPException, APIRouter
from ..database import get_db
from .. import schemas 
from .. import models, oath2
from sqlalchemy.orm import Session
from .. import utils

router = APIRouter(prefix = '/votes', tags = ['VOTE'])


@router.post('/', status_code= status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db: Session = Depends(get_db), current_user: models.User = Depends(oath2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == vote.post_id)
    
    found_post = post_query.first()
    if not found_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {vote.post_id} is not found")
    
    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id)
    
    already_voted = vote_query.first()
     
    if vote.dir == 1:
        if already_voted:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail= f"user {current_user.id} has alredy voted on post {vote.post_id}")
        else:
            new_vote = models.Vote(post_id = vote.post_id, user_id = current_user.id)
            db.add(new_vote)
            db.commit()
            db.refresh(new_vote)
            return {"message": "successfully added vote"}
    
    else:
        if already_voted:
            vote_query.delete(synchronize_session = False)
            db.commit()
            return {"message": "successfully deleted vote"}
        else:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail = "vote doesn't exist")