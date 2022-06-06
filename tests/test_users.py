import pytest
from app import schemas
from jose import jwt
from app.config import settings

def test_root(client):
    res = client.get("/")
    assert res.json().get('message') == 'hello world'
    # print(res.json())
    assert res.status_code == 200
    
def test_create_user(client):
    res = client.post("/users/", json = {"email": "hello@gmail.com", "password": "password123"})
    new_user = schemas.UserOut(**res.json()) # checkinig the response output in json format same as userout
    assert new_user.email == "hello@gmail.com"
    assert res.status_code == 201
    
def test_login(client, test_user):
    res = client.post("/login", data = {"username": test_user['email'], "password": test_user['password']})
    login_response = schemas.Token(**res.json())
    
    payload = jwt.decode(login_response.access_token, settings.secret_key, [settings.algorithm])    
    deduced_user_id = payload.get("user_id")
    assert deduced_user_id == test_user['id']
    assert login_response.type == 'bearer'
    assert res.status_code == 200
    
@pytest.mark.parametrize("email, password, status_code",[
    ('wrongemail@gmail.com', 'password123', 403),
    ('sanjeev@gmail.com', 'wrongpassword', 403),
    ('wrongemail@gmail.com', 'wrongpassword', 403),
    (None, 'password123', 422),
    ('sanjeev@gmail.com', None, 422)
])
def test_incorrect_login(client, test_user, email, password, status_code):
    res = client.post("/login", data = {"username": email, "password": password})
    
    assert res.status_code == status_code
    