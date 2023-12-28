import random
import pytest

from fastapi import status
from fastapi.testclient import TestClient

from .utils import get_access_token


random_number = random.randrange(0, 99999, 1)
random_small_number = random.randrange(1, 5, 1)


# @pytest.mark.skip
@pytest.mark.order(4)
@pytest.mark.parametrize(
    ", ".join(
        [
            "username",
            "password",
            "name",
            "description",
            "status_code",
            "happy_path",
        ]
    ),
    [
        (
            f"user_{random_number}@server-00.com",
            "password123",
            "user1 name1 adress1",
            "Profile test A",
            status.HTTP_201_CREATED,
            True,
        ),
        (
            f"user_{random_number}@server-00.com",
            "password123",
            "user2 name2 adress2",
            "Profile test B",
            status.HTTP_201_CREATED,
            True,
        ),
        (
            f"user_{random_number}@server-00.com",
            "password123",
            "user3 name3 adress3",
            "Profile test C",
            status.HTTP_201_CREATED,
            True,
        ),
    ],
)
def test_create_profile(
    client: TestClient,
    username,
    password,
    name,
    description,
    status_code,
    happy_path,
):
    access_data = {"username": username, "password": password}
    client.post("api/v1/users/sign-up/", json=access_data)
    login_response = client.post(
        "api/v1/users/login/",
        data=access_data,
    )
    access_token = login_response.json()["access_token"]
    create_profile_response = client.post(
        "api/v1/users/profile/",
        json={
            "name": name,
            "description": description,
        },
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert create_profile_response.status_code == status_code
    if happy_path:
        assert "description" in create_profile_response.json()
        assert "name" in create_profile_response.json()
        assert "user" in create_profile_response.json()
        assert "username" in create_profile_response.json()["user"]
    else:
        assert "detail" in create_profile_response.json()


# @pytest.mark.skip
@pytest.mark.order(5)
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
            f"user_{random_number}@server-00.com",
            "password123",
            status.HTTP_200_OK,
            True,
        ),
    ],
)
def test_get_profile(
    client: TestClient,
    username,
    password,
    status_code,
    happy_path,
):
    access_token = get_access_token(client, username, password)
    get_profile_response = client.get(
        "api/v1/users/profile/",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert get_profile_response.status_code == status_code
    if happy_path:
        assert "user" in get_profile_response.json()
        assert "username" in get_profile_response.json()["user"]
        assert "profiles" in get_profile_response.json()
        assert "id" in get_profile_response.json()["profiles"][0]
        assert "name" in get_profile_response.json()["profiles"][0]
        assert "description" in get_profile_response.json()["profiles"][0]
    else:
        assert "detail" in get_profile_response.json()


# @pytest.mark.skip
@pytest.mark.order(6)
@pytest.mark.parametrize(
    ", ".join(
        [
            "username",
            "password",
            "name",
            "description",
            "status_code",
            "happy_path",
        ]
    ),
    [
        (
            f"user_{random_number}@server-00.com",
            "password123",
            "new name",
            "new description",
            status.HTTP_202_ACCEPTED,
            True,
        ),
    ],
)
def test_update_profile(
    client: TestClient,
    username,
    password,
    name,
    description,
    status_code,
    happy_path,
):
    access_token = get_access_token(client, username, password)
    get_profile_response = client.get(
        "api/v1/users/profile/",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    random_profile = random.choice(get_profile_response.json()["profiles"])
    profile_id = random_profile["id"]
    update_profile_url = f"api/v1/users/profile/{profile_id}/"
    update_profile_data = {}
    if name:
        update_profile_data["name"] = name
    if description:
        update_profile_data["description"] = description
    update_profile_response = client.patch(
        update_profile_url,
        json=update_profile_data,
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert update_profile_response.status_code == status_code
    if happy_path:
        assert "name" in update_profile_response.json()
        assert update_profile_response.json()["name"] == name
        assert "description" in update_profile_response.json()
        assert update_profile_response.json()["description"] == description
        assert "user" in update_profile_response.json()
        assert "username" in update_profile_response.json()["user"]
    else:
        assert "detail" in update_profile_response.json()


# @pytest.mark.skip
@pytest.mark.order(7)
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
            f"user_{random_number}@server-00.com",
            "password123",
            status.HTTP_204_NO_CONTENT,
            True,
        ),
    ],
)
def test_delete_profile(
    client: TestClient,
    username,
    password,
    status_code,
    happy_path,
):
    access_token = get_access_token(client, username, password)
    headers = {"Authorization": f"Bearer {access_token}"}
    get_profile_response = client.get("api/v1/users/profile/", headers=headers)
    random_profile = random.choice(get_profile_response.json()["profiles"])
    profile_id = random_profile["id"]
    delete_profile_url = f"api/v1/users/profile/{profile_id}/"
    response = client.delete(delete_profile_url, headers=headers)
    assert response.status_code == status_code
    if happy_path:
        assert response.text == ""
    else:
        assert "detail" in response.json()


# @pytest.mark.skip
@pytest.mark.order(8)
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
            f"user_{random_number}@server-00.com",
            "password123",
            status.HTTP_200_OK,
            True,
        ),
    ],
)
def test_get_other_profiles(
    client: TestClient,
    username,
    password,
    status_code,
    happy_path,
):
    access_token = get_access_token(client, username, password)
    other_profiles_response = client.get(
        "api/v1/users/profile/others/",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert other_profiles_response.status_code == status_code
    if happy_path:
        assert "profiles" in other_profiles_response.json()
        assert "id" in other_profiles_response.json()["profiles"][0]
        assert "user_id" in other_profiles_response.json()["profiles"][0]
        assert "name" in other_profiles_response.json()["profiles"][0]
        assert "description" in other_profiles_response.json()["profiles"][0]
    else:
        assert "detail" in other_profiles_response.json()


# @pytest.mark.skip
@pytest.mark.order(9)
@pytest.mark.parametrize(
    ", ".join(
        [
            "username",
            "password",
            "quantity_of_profiles",
            "status_code",
            "happy_path",
        ]
    ),
    [
        (
            f"user_{random_number}@server-00.com",
            "password123",
            random_small_number,
            status.HTTP_201_CREATED,
            True,
        ),
    ],
)
def test_add_other_profiles_to_my_favorites(
    client: TestClient,
    username,
    password,
    quantity_of_profiles,
    status_code,
    happy_path,
):
    test_endpoint = "api/v1/users/profile/favorites/"
    access_token = get_access_token(client, username, password)
    other_profiles_response = client.get(
        "api/v1/users/profile/others/",
        headers={"Authorization": f"Bearer {access_token}"},
    )
    other_profiles = other_profiles_response.json()["profiles"]
    profiles_add_to_favorites = []
    for i in range(quantity_of_profiles):
        random_profile = random.choice(other_profiles)
        profiles_add_to_favorites.append(random_profile["id"])
    test_response = client.post(
        test_endpoint,
        json={"profile_ids": profiles_add_to_favorites},
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert test_response.status_code == status_code
    if happy_path:
        assert "response" in test_response.json()
    else:
        assert "detail" in test_response.json()


# @pytest.mark.skip
@pytest.mark.order(10)
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
            f"user_{random_number}@server-00.com",
            "password123",
            status.HTTP_200_OK,
            True,
        ),
    ],
)
def test_get_favorite_profiles(
    client: TestClient,
    username,
    password,
    status_code,
    happy_path,
):
    test_endpoint = "api/v1/users/profile/favorites/"
    access_token = get_access_token(client, username, password)
    test_response = client.get(
        test_endpoint,
        headers={"Authorization": f"Bearer {access_token}"},
    )
    assert test_response.status_code == status_code
    if happy_path:
        assert "profiles" in test_response.json()
        assert "id" in test_response.json()["profiles"][0]
        assert "name" in test_response.json()["profiles"][0]
        assert "description" in test_response.json()["profiles"][0]
    else:
        assert "detail" in test_response.json()


# @pytest.mark.skip
@pytest.mark.order(11)
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
            f"user_{random_number}@server-00.com",
            "password123",
            status.HTTP_204_NO_CONTENT,
            True,
        ),
    ],
)
def test_delete_profile_from_favorites(
    client: TestClient,
    username,
    password,
    status_code,
    happy_path,
):
    favorite_profiles_url = "api/v1/users/profile/favorites/"
    access_token = get_access_token(client, username, password)
    headers = {"Authorization": f"Bearer {access_token}"}
    get_favorites_response = client.get(favorite_profiles_url, headers=headers)
    random_profile = random.choice(get_favorites_response.json()["profiles"])
    profile_id = random_profile["id"]
    delete_profile_url = f"api/v1/users/profile/favorites/{profile_id}/"
    response = client.delete(delete_profile_url, headers=headers)
    assert response.status_code == status_code
    if happy_path:
        assert response.text == ""
    else:
        assert "detail" in response.json()
