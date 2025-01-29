from abc import ABC, abstractmethod
from datetime import datetime
from typing import Dict, List, Optional
from openapi_server.models.task import Task


class ITaskRepository(ABC):
    @abstractmethod
    async def create(
        self,
        name: str,
        description: str,
        deadline: datetime,
        completed: bool,
        user_id: int,
    ) -> int:
        pass

    @abstractmethod
    async def find_by_id(self, task_id: int, user_id: int) -> Optional[Task]:
        pass

    @abstractmethod
    async def find_by_user_id(self, user_id: int) -> List[Task]:
        pass

    @abstractmethod
    async def update(self, task: Task, user_id: int) -> Task:
        pass

    @abstractmethod
    async def delete(self, task_id: int, user_id: int) -> None:
        pass


class InMemoryTaskRepository(ITaskRepository):
    def __init__(self):
        self._tasks: Dict[int, Dict[int, Task]] = {}  # user_id -> task_id -> Task
        self._next_id: int = 1

    async def create(
        self,
        name: str,
        description: str,
        deadline: datetime,
        completed: bool,
        user_id: int,
    ) -> int:
        task_id = self._next_id
        self._next_id += 1

        task = Task(
            id=task_id,
            name=name,
            description=description,
            deadline=deadline,
            completed=completed,
        )

        if user_id not in self._tasks:
            self._tasks[user_id] = {}

        self._tasks[user_id][task_id] = task
        return task_id

    async def find_by_id(self, task_id: int, user_id: int) -> Optional[Task]:
        user_tasks = self._tasks.get(user_id, {})
        return user_tasks.get(task_id)

    async def find_by_user_id(self, user_id: int) -> List[Task]:
        user_tasks = self._tasks.get(user_id, {})
        return list(user_tasks.values())

    async def update(self, task: Task, user_id: int) -> Task:
        if user_id not in self._tasks or task.id not in self._tasks[user_id]:
            raise ValueError("指定されたタスクが見つかりません")
        self._tasks[user_id][task.id] = task
        return task

    async def delete(self, task_id: int, user_id: int) -> None:
        if user_id not in self._tasks or task_id not in self._tasks[user_id]:
            raise ValueError("指定されたタスクが見つかりません")
        del self._tasks[user_id][task_id]
