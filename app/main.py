from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI

from .routers import user
from .routers import post, vote
from . import models
from . import auth
from .database import engine
from . import config


origins = ["*"]
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(user.router)
app.include_router(post.router)
app.include_router(auth.router)
app.include_router(vote.router)

# Since this is just creating the postgress tables using sqlalchemy, however not needed with alembic
# models.Base.metadata.create_all(bind = engine)


