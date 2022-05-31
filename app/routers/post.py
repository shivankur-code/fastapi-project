from fastapi import APIRouter, Depends, FastAPI, status, Response, HTTPException
from sqlalchemy import func

from ..database import get_db
from typing import List, Optional
from .. import schemas 
from .. import models
from .. import oath2
from sqlalchemy.orm import Session

router = APIRouter(prefix = '/posts', tags = ['POSTS'])
    
@router.get('/', response_model= List[schemas.PostOut])
def get_all_posts(db: Session = Depends(get_db), current_user: models.User = Depends(oath2.get_current_user), 
    limit: int = 1, skip: int = 0, search: Optional[str] = ""):
    # cursor.execute(""" SELECT * FROM posts""")
    # posts = cursor.fetchall()
    # # code to serialize the post object of db to dictionary
    # columnNames = [column[0] for column in cursor.description]
    # lst = []
    # for post in posts:
    #     lst.append( dict( zip( columnNames , post)))
    
    # return lst
    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit = limit).offset(skip).all()
    # print(posts)
    return posts


@router.get('/{id}', response_model= schemas.PostOut)
def get_post(id: int, db: Session = Depends(get_db), current_user: models.User = Depends(oath2.get_current_user)):
    # cursor.execute(""" SELECT * FROM posts WHERE ID = %s""",(str(id),)) # used %s because of fear of sql injections  
    # post = cursor.fetchone()
    # if not post:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
    
    # # code to serialize the post object of db to dictionary
    # columnNames = [column[0] for column in cursor.description]
    # post = dict(zip( columnNames , post ))
    
    # return post 
    
    # post_query = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id)
    post_query = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id)

    post = post_query.first()
    # NOTE THE OBJECT RETURNED IS (MODELS.POST object, votes) its  a tuple not an object 
    # so postout needs to have object and vote 
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found-------")
    
    return post

@router.post('/', status_code= status.HTTP_201_CREATED, response_model= schemas.Post)
def create(post: schemas.PostCreate, db: Session = Depends(get_db), current_user: models.User = Depends(oath2.get_current_user)):
    # cursor.execute(""" INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""",(post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit()
    # # code to serialize the post object of db to dictionary
    # columnNames = [column[0] for column in cursor.description]
    # new_post = dict(zip( columnNames , new_post ))
    
    # return new_post
    # print(type(current_user))
    new_post = models.Post(**post.dict(), owner_id = current_user.id) # ** is used for converting dictionary to usable form 
    db.add(new_post)
    db.commit()
    # used to return new post
    db.refresh(new_post)
    return new_post

@router.put('/{id}', response_model= schemas.Post)
def update(id: int, post: schemas.PostCreate, db: Session = Depends(get_db), current_user: models.User = Depends(oath2.get_current_user)):
    # cursor.execute(""" UPDATE posts SET title = %s, content= %s, published = %s WHERE id = %s RETURNING * """,(post.title, post.content, post.published, str(id),))
    # updated_post = cursor.fetchone()
    # if not updated_post:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
    # conn.commit()
    
    # # code to serialize the post object of db to dictionary
    # columnNames = [column[0] for column in cursor.description]
    # updated_post = dict(zip( columnNames , updated_post ))
    
    # return updated_post
    
    post_query = db.query(models.Post).filter(models.Post.id == id)
    
    update_post = post_query.first()
    
    if not update_post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
    
    if current_user.id != update_post.owner_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authurized to perform this action")
    
    post_query.update(post.dict(), synchronize_session= False)
    
    db.commit()
    
    return post_query.first()

@router.delete('/{id}', status_code = status.HTTP_204_NO_CONTENT)
def delete(id: int, db: Session = Depends(get_db), current_user: models.User = Depends(oath2.get_current_user)):
    # cursor.execute(""" DELETE FROM posts WHERE id = %s returning *""",(str(id),))
    # deleted_post = cursor.fetchone()
    # if not deleted_post:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
    # conn.commit()
    # return Response(status_code=status.HTTP_204_NO_CONTENT)
    post_query = db.query(models.Post).filter(models.Post.id == id)
    
    post = post_query.first()
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id: {id} was not found")
    
    if current_user.id != post.owner_id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authurized to perform this action")
    
    post_query.delete(synchronize_session= False)
    
    db.commit()
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)
