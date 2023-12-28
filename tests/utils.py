from fastapi.testclient import TestClient


def get_access_token(
    client: TestClient,
    username: str,
    password: str,
):
    login_url = "api/v1/users/login/"
    access_data = {
        "username": username,
        "password": password,
    }
    response = client.post(login_url, data=access_data)
    return response.json()["access_token"]
