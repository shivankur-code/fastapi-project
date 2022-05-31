from fastapi import Depends, FastAPI, status, HTTPException, APIRouter
from requests import Session
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from .database import get_db
from . import schemas, models, utils, oath2

router = APIRouter(tags = ['AUTHENTICATION'])

@router.post('/login',response_model= schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    # user_credentials now contains only 'username' and 'password' by default
    # {
    #     "username": "abc@gmail.com",
    #     "password": "psswd123"
    # }
    user_query = db.query(models.User).filter(models.User.email == user_credentials.username)
    user = user_query.first()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")
    
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")
    
    # login successfull so create and send token that could be used by other api's
    # create token
    # return token
    access_token = oath2.create_token({"user_id": user.id})
    return {"access_token": access_token, "type": "bearer"}
    