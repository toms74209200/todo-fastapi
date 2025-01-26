from abc import ABC, abstractmethod
from typing import Optional, Dict


class IUserRepository(ABC):
    @abstractmethod
    async def create(self, email: str, password_hash: str) -> int:
        pass

    @abstractmethod
    async def find_by_email(self, email: str) -> Optional[Dict]:
        pass


class InMemoryUserRepository(IUserRepository):
    _instance = None
    _users: Dict[int, Dict] = {}
    _next_id = 1

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(InMemoryUserRepository, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        # シングルトンなので初期化は__new__で行う
        pass

    async def create(self, email: str, password_hash: str) -> int:
        user_id = self._next_id
        self._users[user_id] = {
            "id": user_id,
            "email": email,
            "password_hash": password_hash,
        }
        self._next_id += 1
        return user_id

    async def find_by_email(self, email: str) -> Optional[Dict]:
        for user in self._users.values():
            if user["email"] == email:
                return user.copy()
        return None
