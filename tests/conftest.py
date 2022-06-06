import pytest
from fastapi.testclient import TestClient
from app.main import app
from urllib.parse import quote  
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.config import settings
from app.database import get_db
from app.database import Base
from app import models
from app.oath2 import create_token

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
 

@pytest.fixture
#create a user for testing for each path test down here
def test_user(client):
    new_user = {"email": "shiv@gmail.com", "password": "shiv"}
    res = client.post("/users/", json = new_user)
    test_user = res.json()
    test_user['password'] = new_user["password"]
    return test_user

@pytest.fixture
#create a user for testing for each path test down here
def test_user2(client):
    new_user = {"email": "shiv123@gmail.com", "password": "shiv"}
    res = client.post("/users/", json = new_user)
    test_user = res.json()
    test_user['password'] = new_user["password"]
    return test_user
    
@pytest.fixture
def token(test_user):
    return create_token({"user_id": test_user['id']})
    
@pytest.fixture
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }
    return client

@pytest.fixture
def test_posts(test_user, session, test_user2):
    posts_data = [{
        "title": "first title",
        "content": "first content",
        "owner_id": test_user['id']
    }, {
        "title": "2nd title",
        "content": "2nd content",
        "owner_id": test_user['id']
    },
        {
        "title": "3rd title",
        "content": "3rd content",
        "owner_id": test_user['id']
    },
        {
        "title": "4th title",
        "content": "4th content",
        "owner_id": test_user2['id']
    }]
    
    # def create_post(post):
    #     return models.Post(**post)
    
    # posts_map = map(create_post, posts_data)
    # posts_list = list(posts_map)
    # session.add_all(posts_list)
    session.add_all([models.Post(**posts_data[0]), models.Post(**posts_data[1]), models.Post(**posts_data[2]), models.Post(**posts_data[3])])
    
    session.commit()
    # print(posts_list,"___________________>-------")
    posts = session.query(models.Post).all()
    # print(posts,"___________________>-------")
    return posts