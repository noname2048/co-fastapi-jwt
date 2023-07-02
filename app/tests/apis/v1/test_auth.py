from fastapi import status
from fastapi.testclient import TestClient


def test_signup_and_signin(client: TestClient) -> None:
    fake_email = "test@test.com"
    fake_password = "test1234"

    response = client.post(
        "/api/v1/token/login",
        data={
            "email": fake_email,
            "password": fake_password,
        },
    )

    assert response.status_code == status.HTTP_201_CREATED, response.status_code
    assert response.json()["uuid"].len() == 36
