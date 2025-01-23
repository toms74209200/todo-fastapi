# coding: utf-8

from typing import ClassVar, Dict, List, Tuple  # noqa: F401

from pydantic import Field, StrictInt
from typing import Any, List, Optional
from typing_extensions import Annotated
from openapi_server.models.post_tasks_request import PostTasksRequest
from openapi_server.models.put_tasks_request import PutTasksRequest
from openapi_server.models.task import Task
from openapi_server.models.task_id import TaskId
from openapi_server.security_api import get_token_BearerAuth

class BaseTasksApi:
    subclasses: ClassVar[Tuple] = ()

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        BaseTasksApi.subclasses = BaseTasksApi.subclasses + (cls,)
    async def delete_tasks(
        self,
        taskId: StrictInt,
    ) -> None:
        """指定したタスクを削除する。"""
        ...


    async def get_tasks(
        self,
        user_id: Annotated[StrictInt, Field(description="取得するタスクのユーザーID")],
    ) -> List[Task]:
        """指定したユーザーのタスク一覧を取得する。"""
        ...


    async def post_tasks(
        self,
        post_tasks_request: Optional[PostTasksRequest],
    ) -> TaskId:
        """タスクを登録する。"""
        ...


    async def put_tasks(
        self,
        taskId: Annotated[StrictInt, Field(description="更新するタスクのID")],
        put_tasks_request: Optional[PutTasksRequest],
    ) -> Task:
        """指定したタスクを更新する。"""
        ...
