from abc import ABC, abstractmethod
from datetime import datetime
from typing import Dict, List, Optional
from openapi_server.models.task import Task


class ITaskRepository(ABC):
    @abstractmethod
    async def create(
        self, name: str, description: str, deadline: datetime, completed: bool
    ) -> int:
        pass

    @abstractmethod
    async def find_by_id(self, task_id: int) -> Optional[Task]:
        pass

    @abstractmethod
    async def find_by_user_id(self, user_id: int) -> List[Task]:
        pass

    @abstractmethod
    async def update(self, task: Task) -> Task:
        pass

    @abstractmethod
    async def delete(self, task_id: int) -> None:
        pass


class InMemoryTaskRepository(ITaskRepository):
    def __init__(self):
        self._tasks: Dict[int, Task] = {}
        self._next_id: int = 1

    async def create(
        self, name: str, description: str, deadline: datetime, completed: bool
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
        self._tasks[task_id] = task
        return task_id

    async def find_by_id(self, task_id: int) -> Optional[Task]:
        return self._tasks.get(task_id)

    async def find_by_user_id(self, user_id: int) -> List[Task]:
        return [task for task in self._tasks.values()]

    async def update(self, task: Task) -> Task:
        if task.id not in self._tasks:
            raise ValueError("指定されたタスクが見つかりません")
        self._tasks[task.id] = task
        return task

    async def delete(self, task_id: int) -> None:
        if task_id not in self._tasks:
            raise ValueError("指定されたタスクが見つかりません")
        del self._tasks[task_id]
