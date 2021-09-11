from app import schemas


def test_get_all_posts(authorized_client, test_posts):

    response = authorized_client.get(
        "/posts")
    print(response.json())
    assert response.status_code == 200
    assert len(response.json()) == len(test_posts)


def test_unauthorized_user_get_all_posts(client, test_posts):
    response = client.get(
        "/posts")
    assert response.status_code == 401


def test_get_post_by_id(authorized_client, test_posts):
    response = authorized_client.get(
        f"/posts/{test_posts[0].id}")
    print(response.json())
    print(test_posts[0].__dict__['title'])
    assert response.json().get('Post').get(
        'title') == test_posts[0].__dict__['title']
    assert response.status_code == 200


def test_unauthorized_user_get_one_posts(client, test_posts):
    response = client.get(
        f"/posts/{test_posts[0].id}")
    assert response.status_code == 401


def test_get_non_exist_post(authorized_client, test_user, test_posts):
    response = authorized_client.get(
        f"/posts/{50000}")

    assert response.status_code == 404


def test_create_post(authorized_client, test_user, test_posts):
    response = authorized_client.post(
        "/posts", json={"title": "created post test title", "content": "created post test content", "published": False})

    created_post = schemas.Post(**response.json())
    assert created_post.title == "created post test title"
    assert created_post.content == "created post test content"
    assert created_post.owner_id == test_user['id']
    assert created_post.published == False
    assert response.status_code == 201


def test_create_post_default_published(authorized_client, test_user, test_posts):
    response = authorized_client.post(
        "/posts", json={"title": "created post test title", "content": "created post test content"})

    created_post = schemas.Post(**response.json())
    assert created_post.published == True
    assert response.status_code == 201


def test_delete_post(authorized_client, test_user, test_posts):
    response = authorized_client.delete(
        f"/posts/{test_posts[0].id}")

    assert response.status_code == 204


def test_delete_non_exist_post(authorized_client, test_user, test_posts):
    response = authorized_client.delete(
        f"/posts/{50000}")

    assert response.status_code == 404


def test_delete_other_user_post(authorized_client, test_user, test_posts):
    response = authorized_client.delete(
        f"/posts/{test_posts[2].id}")

    assert response.status_code == 403


def test_update_post(authorized_client, test_user, test_posts):
    data = {
        "title": "updated title",
        "content": "updatd content",
        "id": test_posts[0].id

    }

    response = authorized_client.put(
        f"/posts/{test_posts[0].id}", json=data)

    updated_post = schemas.Post(**response.json())
    assert response.status_code == 200
    assert updated_post.title == data['title']
    assert updated_post.content == data['content']


def test_update_other_user_post(authorized_client, test_user, test_user2, test_posts):
    data = {
        "title": "updated title",
        "content": "updatd content",
        "id": test_posts[2].id

    }
    response = authorized_client.put(
        f"/posts/{test_posts[2].id}", json=data)

    assert response.status_code == 403
