from typing import Optional
from pydantic import BaseModel, EmailStr
from datetime import datetime
from pydantic.types import conint
      
class UserCreate(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    class Config:
        orm_mode = True
        
class UserLogin(BaseModel):
    email: EmailStr
    password: str
    class Config:
        orm_mode = True
        

class PostCreate(BaseModel):
    title: str
    content: str
    published: bool = True
    

class Post(PostCreate):
    id: int
    created_at: datetime
    owner: UserOut
    class Config:
        orm_mode = True
        
class PostOut(BaseModel):
    Post: Post
    votes: int
    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    type: str
    class Config:
        orm_mode = True
    
class TokenData(BaseModel):
    user_id: Optional[str] = None
    
class Vote(BaseModel):
    post_id: int
    dir: conint(le=1)