# coding: utf-8

from typing import Dict, List  # noqa: F401
import importlib
import pkgutil

from openapi_server.apis.tasks_api_base import BaseTasksApi
import openapi_server.impl

from fastapi import (  # noqa: F401
    APIRouter,
    Body,
    Cookie,
    Depends,
    Form,
    Header,
    HTTPException,
    Path,
    Query,
    Response,
    Security,
    status,
)

from openapi_server.models.extra_models import TokenModel  # noqa: F401
from pydantic import Field, StrictInt
from typing import Any, List, Optional
from typing_extensions import Annotated
from openapi_server.models.post_tasks_request import PostTasksRequest
from openapi_server.models.put_tasks_request import PutTasksRequest
from openapi_server.models.task import Task
from openapi_server.models.task_id import TaskId
from openapi_server.security_api import get_token_BearerAuth

router = APIRouter()

ns_pkg = openapi_server.impl
for _, name, _ in pkgutil.iter_modules(ns_pkg.__path__, ns_pkg.__name__ + "."):
    importlib.import_module(name)


@router.delete(
    "/tasks/{taskId}",
    responses={
        204: {"description": "Delete Succeeded"},
        400: {"description": "Bad Request"},
        401: {"description": "Unauthorized"},
        404: {"description": "Not Found"},
    },
    tags=["tasks"],
    summary="タスク削除API",
    response_model_by_alias=True,
)
async def delete_tasks(
    taskId: StrictInt = Path(..., description=""),
    token_BearerAuth: TokenModel = Security(get_token_BearerAuth),
) -> None:
    """指定したタスクを削除する。"""
    if not BaseTasksApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseTasksApi.subclasses[0]().delete_tasks(taskId)


@router.get(
    "/tasks",
    responses={
        200: {
            "model": List[Task],
            "description": "指定されたユーザーのタスク一覧が返されます",
        },
        400: {"description": "Bad Request"},
        401: {"description": "Unauthorized"},
        404: {"description": "Not Found"},
    },
    tags=["tasks"],
    summary="ユーザーのタスク一覧取得API",
    response_model_by_alias=True,
)
async def get_tasks(
    user_id: Annotated[
        StrictInt, Field(description="取得するタスクのユーザーID")
    ] = Query(None, description="取得するタスクのユーザーID", alias="userId"),
    token_BearerAuth: TokenModel = Security(get_token_BearerAuth),
) -> List[Task]:
    """指定したユーザーのタスク一覧を取得する。"""
    if not BaseTasksApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseTasksApi.subclasses[0]().get_tasks(user_id, token_BearerAuth)


@router.post(
    "/tasks",
    responses={
        201: {"model": TaskId, "description": "新しいタスクが作成されました"},
        400: {"description": "Bad Request"},
        401: {"description": "Unauthorized"},
    },
    tags=["tasks"],
    summary="タスク登録API",
    response_model_by_alias=True,
)
async def post_tasks(
    post_tasks_request: Optional[PostTasksRequest] = Body(None, description=""),
    token_BearerAuth: TokenModel = Security(get_token_BearerAuth),
) -> TaskId:
    """タスクを登録する。"""
    if not BaseTasksApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseTasksApi.subclasses[0]().post_tasks(
        post_tasks_request, token_BearerAuth
    )


@router.put(
    "/tasks/{taskId}",
    responses={
        200: {"model": Task, "description": "更新されたタスクが返されます"},
        400: {"description": "Bad Request"},
        401: {"description": "Unauthorized"},
        404: {"description": "Not Found"},
    },
    tags=["tasks"],
    summary="タスク更新API",
    response_model_by_alias=True,
)
async def put_tasks(
    taskId: Annotated[StrictInt, Field(description="更新するタスクのID")] = Path(
        ..., description="更新するタスクのID"
    ),
    put_tasks_request: Optional[PutTasksRequest] = Body(None, description=""),
    token_BearerAuth: TokenModel = Security(get_token_BearerAuth),
) -> Task:
    """指定したタスクを更新する。"""
    if not BaseTasksApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseTasksApi.subclasses[0]().put_tasks(
        taskId, put_tasks_request, token_BearerAuth
    )
