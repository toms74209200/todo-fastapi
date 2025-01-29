from datetime import datetime
from typing import List, Optional
from openapi_server.models.task import Task
from openapi_server.repositories.task_repository import ITaskRepository


class TaskService:
    def __init__(self, task_repository: ITaskRepository):
        self._repository = task_repository

    async def create_task(
        self,
        name: str,
        description: str,
        deadline: datetime,
        completed: bool,
        user_id: int,
    ) -> int:
        if not name:
            raise ValueError("タスク名は必須です")

        if not description:
            raise ValueError("説明は必須です")

        if not deadline:
            raise ValueError("期限は必須です")

        if not user_id:
            raise ValueError("ユーザーIDは必須です")

        return await self._repository.create(
            name=name,
            description=description,
            deadline=deadline,
            completed=completed,
            user_id=user_id,
        )
