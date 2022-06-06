from app import schemas
import pytest

def test_get_all_posts(authorized_client, test_posts):
    res = authorized_client.get("/posts/") # note that res contains {Post{ Post_object }, votes}
    def validate(post):
        return schemas.Post(**post)
    posts_map = map(validate, res.json())
    assert len(res.json()) == len(test_posts)
    assert res.status_code == 200
    
def test_unauthorized_get_posts(client, test_posts):
    res = client.get("/posts/")
    assert res.status_code == 401
    
def test_unauthorized_get_one_post(client, test_posts):
    res = client.get(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401

def test_get_one_post_not_exist(authorized_client, test_posts):
    res = authorized_client.get("/posts/7888")
    assert res.status_code == 404

def test_get_one_post(authorized_client, test_posts):
    res = authorized_client.get(f"/posts/{test_posts[0].id}")
    post = schemas.PostOut(**res.json())
    # print(res.json(),"--------->", test_posts)
    assert post.Post.id == test_posts[0].id
    assert post.Post.title == test_posts[0].title
    assert post.Post.content == test_posts[0].content
    assert res.status_code == 200

@pytest.mark.parametrize("title, content, published", [
    ("awesome new title", "awesome new content", True),
    ("favorite pizza", "i love pepperoni", False),
    ("tallest skyscrapers", "wahoo", True),
])
def test_create_posts(title, content, published, authorized_client, test_user):
    res = authorized_client.post("/posts/", json = {"title": title, "content": content, "published": published})
    created_post = schemas.Post(**res.json())
    assert res.status_code == 201
    assert created_post.owner.id == test_user['id']
    assert created_post.title == title
    assert created_post.content == content
    assert created_post.published == published
    
def test_create_posts_default_published(authorized_client, test_user):
    res = authorized_client.post("/posts/", json = {"title": "arbitrary title", "content": "aasdfjasdf"})
    created_post = schemas.Post(**res.json())
    assert res.status_code == 201
    assert created_post.owner.id == test_user['id']
    assert created_post.published == True
    
def test_unauthorized_user_create_post(client, test_user):
    res = client.post("/posts/", json = {"title": "arbitrary title", "content": "aasdfjasdf"})
    assert res.status_code == 401
    
def test_unauthorized_user_delete_post(client, test_user, test_posts):
    res = client.delete(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401
    
def test_user_delete_post(authorized_client, test_user, test_posts):
    res = authorized_client.delete(f"/posts/{test_posts[0].id}")
    assert res.status_code == 204

def test_delete_post_not_exist(authorized_client, test_user, test_posts):
    res = authorized_client.delete(f"/posts/0989")
    assert res.status_code == 404
    
def test_delete_other_user_post(authorized_client, test_user, test_posts):
    # authorized_client is logged in as test_user1 and test_posts[3] is the post with owner_id as of test_user2
    res = authorized_client.delete(f"/posts/{test_posts[3].id}")
    assert res.status_code == 403

def test_update_post(authorized_client, test_user, test_posts):
    data = {
        "title": "updated title",
        "content": "updatd content",
        "id": test_posts[0].id
    }
    res = authorized_client.put(f"/posts/{test_posts[0].id}", json = data)
    assert res.status_code == 200
    # assert res.status_code == 200

def test_update_other_user_post(authorized_client, test_user, test_user2, test_posts):
    data = {
        "title": "updated title",
        "content": "updatd content",
        "id": test_posts[0].id
    }
    # authorized client as test_user and updating the post owned by test_user2
    res = authorized_client.put(f"/posts/{test_posts[3].id}", json = data)
    assert res.status_code == 403

def test_unauthorized_update_post(client, test_user, test_posts):
    data = {
        "title": "updated title",
        "content": "updatd content",
        "id": test_posts[0].id
    }
    res = client.put(f"/posts/{test_posts[0].id}", json = data)
    assert res.status_code == 401
    
def test_update_post_not_exist(authorized_client, test_user, test_posts):
    data = {
        "title": "updated title",
        "content": "updatd content",
        "id": test_posts[0].id
    }
    res = authorized_client.put(f"/posts/0989", json = data)
    assert res.status_code == 404