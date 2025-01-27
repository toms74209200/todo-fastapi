from typing import List, Optional, Annotated
from fastapi import HTTPException, Header, Response, status, Depends, Security
from datetime import datetime
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from openapi_server.services.auth_service import verify_token

from openapi_server.apis.tasks_api_base import BaseTasksApi
from openapi_server.models.post_tasks_request import PostTasksRequest
from openapi_server.models.put_tasks_request import PutTasksRequest
from openapi_server.models.task import Task
from openapi_server.models.task_id import TaskId
from openapi_server.repositories.task_repository import InMemoryTaskRepository
from openapi_server.services.task_service import TaskService
from openapi_server.models.extra_models import TokenModel
from openapi_server.security_api import get_token_BearerAuth

security = HTTPBearer()


class TasksApiImpl(BaseTasksApi):
    _instance = None
    _repository = None
    _service = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(TasksApiImpl, cls).__new__(cls)
            cls._repository = InMemoryTaskRepository()
            cls._service = TaskService(cls._repository)
        return cls._instance

    def __init__(self):
        # シングルトンなので初期化は__new__で行う
        pass

    async def post_tasks(
        self,
        post_tasks_request: Optional[PostTasksRequest] = None,
        token_BearerAuth: TokenModel = Security(get_token_BearerAuth),
    ) -> Response:
        """
        タスク作成の実装
        """

        if post_tasks_request is None:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="タスク情報が必要です",
            )

        if not isinstance(post_tasks_request.name, str):
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="タスク名は文字列である必要があります",
            )

        if not isinstance(post_tasks_request.description, str):
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="説明は文字列である必要があります",
            )

        if not isinstance(post_tasks_request.deadline, datetime):
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="期限は日時形式である必要があります",
            )

        try:
            task_id = await self._service.create_task(
                name=post_tasks_request.name,
                description=post_tasks_request.description,
                deadline=post_tasks_request.deadline,
                completed=post_tasks_request.completed or False,
            )
            return Response(
                status_code=status.HTTP_201_CREATED,
                content=TaskId(id=task_id).model_dump_json(),
                media_type="application/json",
            )
        except ValueError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
