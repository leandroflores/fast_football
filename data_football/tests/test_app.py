from http import HTTPStatus

from fastapi.testclient import TestClient
from httpx import Response


def test_home(client: TestClient):
    # Act
    response: Response = client.get("/")

    # Assert
    assert response.status_code == HTTPStatus.OK
    assert response.json() == {"message": "Data Football Service!"}
