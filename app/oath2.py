from datetime import datetime, timedelta
import imp

from sqlalchemy.orm import Session

from .database import get_db
from . import models
from fastapi import Depends, status, HTTPException
from jose import jwt, JWTError
from . import schemas
from fastapi.security import OAuth2PasswordBearer
from .config import settings


# to get a string like this run:
# openssl rand -hex 32
SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES

oauth_scheme = OAuth2PasswordBearer(tokenUrl="login")

def create_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, ALGORITHM)
    
    return encoded_jwt

def verify_access_token(token: str, credentials_Exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, [ALGORITHM])
        
        deduced_user_id = payload.get("user_id")
        
        if deduced_user_id == None:
            raise credentials_Exception
        
        token_data = schemas.TokenData(user_id = deduced_user_id)
    except JWTError:
        raise credentials_Exception
    
    return token_data

# get_current_user from token data
def get_current_user(token: str = Depends(oauth_scheme), db: Session = Depends(get_db)):
    credentials_Exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})
    
    token = verify_access_token(token, credentials_Exception)
    user = db.query(models.User).filter(models.User.id == token.user_id).first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    
    return user