from fastapi import Depends, FastAPI, status, HTTPException, APIRouter
from ..database import get_db
from .. import schemas 
from .. import models
from sqlalchemy.orm import Session
from .. import utils

router = APIRouter(prefix = '/users', tags = ['USERS'])

@router.post('/', status_code= status.HTTP_201_CREATED, response_model= schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # hash the password
    user.password = utils.hash(user.password)
    
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get('/{id}', response_model= schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    query_user = db.query(models.User).filter(models.User.id == id)
    user = query_user.first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    
    return user