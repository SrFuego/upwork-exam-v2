import pytest

from jose import jwt

from fastapi import status
from fastapi.testclient import TestClient

from ..src.hex.application.use_cases.auth import ALGORITHM

from .utils import get_access_token


# @pytest.mark.skip
@pytest.mark.order(1)
@pytest.mark.parametrize(
    ", ".join(
        [
            "username",
            "password",
            "status_code",
            "happy_path",
        ]
    ),
    [
        (
            "user_00@server-00.com",
            "password123",
            status.HTTP_201_CREATED,
            True,
        ),
        (
            "user_01@server-00.com",
            "password123",
            status.HTTP_201_CREATED,
            True,
        ),
        (
            "user_02@server-00.com",
            "123password",
            status.HTTP_201_CREATED,
            True,
        ),
        (
            "user_03@server-01.xyz",
            "Pa$$w0rd123xyz",
            status.HTTP_201_CREATED,
            True,
        ),
        (
            "user_04@server-01.xyz",
            "123",
            status.HTTP_422_UNPROCESSABLE_ENTITY,
            False,
        ),
        (
            "user_05@server-02.com",
            "",
            status.HTTP_422_UNPROCESSABLE_ENTITY,
            False,
        ),
        (
            "",
            "password123",
            status.HTTP_422_UNPROCESSABLE_ENTITY,
            False,
        ),
        (
            "",
            "",
            status.HTTP_422_UNPROCESSABLE_ENTITY,
            False,
        ),
        (
            "user_08",
            "password123",
            status.HTTP_422_UNPROCESSABLE_ENTITY,
            False,
        ),
        (
            "user_00@server-00.com",
            "password123",
            status.HTTP_400_BAD_REQUEST,
            False,
        ),
    ],
)
def test_create_user(
    client: TestClient,
    username,
    password,
    status_code,
    happy_path,
):
    response = client.post(
        "api/v1/users/sign-up/",
        json={
            "username": username,
            "password": password,
        },
    )
    assert response.status_code == status_code
    if happy_path:
        assert response.json() == {
            "response": "User created",
        }
    else:
        assert "detail" in response.json()


# @pytest.mark.skip
@pytest.mark.order(2)
@pytest.mark.parametrize(
    ", ".join(
        [
            "username",
            "password",
            "status_code",
            "happy_path",
        ]
    ),
    [
        (
            "user_00@server-00.com",
            "password123",
            status.HTTP_200_OK,
            True,
        ),
        (
            "user_00@server-00.com",
            "123password",
            status.HTTP_401_UNAUTHORIZED,
            False,
        ),
        (
            "user_00@server-00.com",
            "",
            status.HTTP_422_UNPROCESSABLE_ENTITY,
            False,
        ),
        (
            "user_00@server-00.com",
            "123password",
            status.HTTP_401_UNAUTHORIZED,
            False,
        ),
        (
            "user_03@server-01.xyz",
            "Pa$$w0rd123xyz",
            status.HTTP_200_OK,
            True,
        ),
        (
            "user_04@server-02.com",
            "",
            status.HTTP_422_UNPROCESSABLE_ENTITY,
            False,
        ),
        (
            "",
            "password123",
            status.HTTP_422_UNPROCESSABLE_ENTITY,
            False,
        ),
        (
            "",
            "",
            status.HTTP_422_UNPROCESSABLE_ENTITY,
            False,
        ),
    ],
)
def test_login(
    client: TestClient,
    username,
    password,
    status_code,
    happy_path,
):
    response = client.post(
        "api/v1/users/login/",
        data={
            "username": username,
            "password": password,
        },
    )
    assert response.status_code == status_code
    if happy_path:
        assert "access_token" in response.json()
        assert jwt.get_unverified_header(
            response.json()["access_token"],
        ) == {
            "alg": ALGORITHM,
            "typ": "JWT",
        }
    else:
        assert "detail" in response.json()


# @pytest.mark.skip
@pytest.mark.order(3)
@pytest.mark.parametrize(
    ", ".join(
        [
            "username",
            "password",
            "with_token",
            "status_code",
            "happy_path",
        ]
    ),
    [
        (
            "user_00@server-00.com",
            "password123",
            False,
            status.HTTP_401_UNAUTHORIZED,
            False,
        ),
        (
            "user_00@server-00.com",
            "password123",
            True,
            status.HTTP_204_NO_CONTENT,
            True,
        ),
        (
            "user_01@server-00.com",
            "password123",
            True,
            status.HTTP_204_NO_CONTENT,
            True,
        ),
        (
            "user_02@server-00.com",
            "123password",
            True,
            status.HTTP_204_NO_CONTENT,
            True,
        ),
        (
            "user_03@server-01.xyz",
            "Pa$$w0rd123xyz",
            True,
            status.HTTP_204_NO_CONTENT,
            True,
        ),
    ],
)
def test_delete_user(
    client: TestClient,
    username,
    password,
    with_token,
    status_code,
    happy_path,
):
    delete_user_url = "api/v1/users/"
    access_token = get_access_token(client, username, password)
    headers = {"Authorization": f"Bearer {access_token}"}
    if with_token:
        response = client.delete(delete_user_url, headers=headers)
    else:
        response = client.delete(delete_user_url)

    assert response.status_code == status_code
    if happy_path:
        assert response.text == ""
    else:
        assert "detail" in response.json()
