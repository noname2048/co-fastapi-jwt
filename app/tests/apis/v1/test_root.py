import pytest
from fastapi.testclient import TestClient


def test_root(client):
    response = client.get("/")
    assert response.status_code == 200
