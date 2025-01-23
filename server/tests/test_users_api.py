# coding: utf-8

from fastapi.testclient import TestClient


from typing import Any, Optional  # noqa: F401
from openapi_server.models.post_users201_response import PostUsers201Response  # noqa: F401
from openapi_server.models.user_credentials import UserCredentials  # noqa: F401


def test_post_users(client: TestClient):
    """Test case for post_users

    ユーザー登録API
    """
    user_credentials = {"password":"password","email":"email"}

    headers = {
    }
    # uncomment below to make a request
    #response = client.request(
    #    "POST",
    #    "/users",
    #    headers=headers,
    #    json=user_credentials,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200

