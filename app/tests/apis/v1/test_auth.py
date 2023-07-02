from fastapi.testclient import TestClient


def test_signup_and_login(client: TestClient) -> None:
    fake_email = "test@test.com"
    fake_password = "test1234"

    response = client.post(
        "/api/v1/auth/signup",
        json={
            "email": fake_email,
            "password": fake_password,
        },
    )

    assert response.status_code == 200, response.text
    assert len(response.json()["uuid"]) == 36

    response = client.post(
        "/api/v1/auth/login",
        json={
            "email": fake_email,
            "password": fake_password,
        },
    )

    assert response.status_code == 200, response.text
    assert response.json()["access_token"]
    assert response.json()["refresh_token"]
