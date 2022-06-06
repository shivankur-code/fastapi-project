import imp
import pytest
from app import models

@pytest.fixture()
# it'll vote on behalf of test_user1 on post owned by test_user2
def test_vote(test_user, test_posts, session):
    new_vote = models.Vote(post_id = test_posts[3].id, user_id = test_user['id'])
    session.add(new_vote)
    session.commit()

def test_vote_on_post(authorized_client, test_posts):
    # test_user1 voting on post owned by test_user2
    res = authorized_client.post("/votes/", json = {"post_id": test_posts[3].id, "dir": 1})
    assert res.status_code == 201
    
def test_vote_twice_post(authorized_client, test_posts, test_vote):
    # test_user1 voting twice on post owned by test_user2
    res = authorized_client.post("/votes/", json = {"post_id": test_posts[3].id, "dir": 1})
    assert res.status_code == 409

def test_delete_vote(authorized_client, test_posts, test_vote):
    # test_user1 deleting post owned by test_user2 and voted using test_post
    res = authorized_client.post("/votes/", json = {"post_id": test_posts[3].id, "dir": 0})
    assert res.status_code == 201

def test_delete_vote_non_exist(authorized_client, test_posts):
    # test_user1 deleting post owned by test_user2 and not voted using test_post
    res = authorized_client.post("/votes/", json = {"post_id": test_posts[3].id, "dir": 0})
    assert res.status_code == 404
    
def test_vote_non_exist(authorized_client, test_posts):
    # test_user1 deleting non-existent post 
    res = authorized_client.post("/votes/", json = {"post_id": 435900, "dir": 1})
    assert res.status_code == 404
    
def test_vote_unauthorized_user(client, test_posts):
    # test_user1 deleting non-existent post 
    res = client.post("/votes/", json = {"post_id": test_posts[3].id, "dir": 1})
    assert res.status_code == 401
