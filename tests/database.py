import pytest
from fastapi.testclient import TestClient
from app.main import app
from urllib.parse import quote  
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.config import settings
from app.database import get_db
from app.database import Base

# WE CAN HARDCODE WITH ALL THE DETAILS HERE
engine = create_engine(f'postgresql://{settings.database_username}:%s@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test'%quote(f'{settings.database_password}'))

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture() # scope="module" should not be done to keep all individual tests independent (eg:- keep login and create_user independent), keep default = "function"
def session():
    # start afresh table
    Base.metadata.drop_all(bind = engine)
    # establish the connection with postgres
    Base.metadata.create_all(bind = engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
    

@pytest.fixture
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()
    app.dependency_overrides[get_db] = override_get_db
    
    yield TestClient(app) # this will return client and after completely using the client  moves to next lineobj

    # put the code you want to run after testing all the user endpoints
    # 2. drop all tables after testing to avoid interference in next testing 
    # Base.metadata.drop_all(bind = engine)
 
