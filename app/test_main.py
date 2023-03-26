from fastapi.testclient import TestClient

from .models import Item, User


def test_create_user(client: TestClient):
    response = client.post(
        "/users/", json={"email": "foo@bar.com", "password": "abc123"}
    )
    assert response.status_code == 200, response.content
    assert response.json() == {
        "id": 1,
        "email": "foo@bar.com",
        "is_active": True,
        "items": [],
    }


def test_create_user__duplicate(client: TestClient, create):
    create(User(email="foo@bar.com"))

    response = client.post(
        "/users/", json={"email": "foo@bar.com", "password": "abc123"}
    )

    assert response.status_code == 400, response.content
    assert response.json() == {"detail": "Email already registered"}


def test_read_users(client: TestClient, create):
    create(User(email="foo@bar.com"))
    create(User(email="baz@example.com"))

    response = client.get("/users/")

    assert response.status_code == 200, response.content
    assert response.json() == [
        {"id": 1, "email": "foo@bar.com", "is_active": True, "items": []},
        {"id": 2, "email": "baz@example.com", "is_active": True, "items": []},
    ]


def test_read_user(client: TestClient, create):
    user = create(User(email="foo@bar.com"))
    create(User(email="baz@example.com"))
    create(Item(title="Foo Bar", description="Sample Text", owner=user))

    response = client.get("/users/1/")

    assert response.status_code == 200, response.content
    assert response.json() == {
        "id": 1,
        "email": "foo@bar.com",
        "is_active": True,
        "items": [
            {
                "id": 1,
                "title": "Foo Bar",
                "description": "Sample Text",
                "owner_id": 1,
            }
        ],
    }


def test_read_items(client: TestClient, create):
    user = create(User(email="a@b.com"))
    create(Item(title="Foo Bar", description="Sample Text", owner=user))

    response = client.get("/items/")

    assert response.status_code == 200, response.content
    assert response.json() == [
        {"id": 1, "title": "Foo Bar", "description": "Sample Text", "owner_id": user.id}
    ]
