import pytest
from app import models


@pytest.fixture()
def test_vote(authorized_client, test_posts, session, test_user):
    # new_post = models.Post(title="my new title", content="my new content")
    new_vote = models.Vote(post_id=test_posts[0].id, user_id=test_user['id'])
    session.add(new_vote)
    session.commit()


def test_vote_on_post(authorized_client, test_posts):
    response = authorized_client.post(
        "/vote", json={"post_id": test_posts[0].id, "dir": 1})

    assert response.status_code == 201


def test_vote_twice_post(authorized_client, test_posts, test_vote):
    response = authorized_client.post(
        "/vote", json={"post_id": test_posts[0].id, "dir": 1})
    assert response.status_code == 409


def test_delete_vote(authorized_client, test_posts, test_vote):
    response = authorized_client.post(
        "/vote", json={"post_id": test_posts[0].id, "dir": 0})
    assert response.status_code == 201


def test_delete_non_exist_vote(authorized_client, test_posts, test_vote):
    response = authorized_client.post(
        "/vote", json={"post_id": test_posts[1].id, "dir": 0})
    assert response.status_code == 404


def test_delete_vote_non_exit_post(authorized_client, test_posts, test_vote):
    response = authorized_client.post(
        "/vote", json={"post_id": 5000, "dir": 0})
    assert response.status_code == 404
