# coding: utf-8

from fastapi.testclient import TestClient


from pydantic import Field, StrictInt  # noqa: F401
from typing import Any, List, Optional  # noqa: F401
from typing_extensions import Annotated  # noqa: F401
from openapi_server.models.post_tasks_request import PostTasksRequest  # noqa: F401
from openapi_server.models.put_tasks_request import PutTasksRequest  # noqa: F401
from openapi_server.models.task import Task  # noqa: F401
from openapi_server.models.task_id import TaskId  # noqa: F401


def test_delete_tasks(client: TestClient):
    """Test case for delete_tasks

    タスク削除API
    """

    headers = {
        "Authorization": "Bearer special-key",
    }
    # uncomment below to make a request
    #response = client.request(
    #    "DELETE",
    #    "/tasks/{taskId}".format(taskId=56),
    #    headers=headers,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_get_tasks(client: TestClient):
    """Test case for get_tasks

    ユーザーのタスク一覧取得API
    """
    params = [("user_id", 56)]
    headers = {
        "Authorization": "Bearer special-key",
    }
    # uncomment below to make a request
    #response = client.request(
    #    "GET",
    #    "/tasks",
    #    headers=headers,
    #    params=params,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_post_tasks(client: TestClient):
    """Test case for post_tasks

    タスク登録API
    """
    post_tasks_request = {"name":"string","description":"string","deadline":"2019-08-24T14:15:22Z","completed":false}

    headers = {
        "Authorization": "Bearer special-key",
    }
    # uncomment below to make a request
    #response = client.request(
    #    "POST",
    #    "/tasks",
    #    headers=headers,
    #    json=post_tasks_request,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_put_tasks(client: TestClient):
    """Test case for put_tasks

    タスク更新API
    """
    put_tasks_request = openapi_server.PutTasksRequest()

    headers = {
        "Authorization": "Bearer special-key",
    }
    # uncomment below to make a request
    #response = client.request(
    #    "PUT",
    #    "/tasks/{taskId}".format(taskId=56),
    #    headers=headers,
    #    json=put_tasks_request,
    #)

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200

