from typing import Optional
import re
from fastapi import HTTPException, status

from openapi_server.apis.users_api_base import BaseUsersApi
from openapi_server.models.post_users201_response import PostUsers201Response
from openapi_server.models.user_credentials import UserCredentials
from openapi_server.repositories.user_repository import InMemoryUserRepository
from openapi_server.services.user_service import UserService


class UsersApiImpl(BaseUsersApi):
    _instance = None
    _repository = None
    _service = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(UsersApiImpl, cls).__new__(cls)
            cls._repository = InMemoryUserRepository()
            cls._service = UserService(cls._repository)
        return cls._instance

    def __init__(self):
        # シングルトンなので初期化は__new__で行う
        pass

    def _validate_email(self, email: str) -> bool:
        pattern = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        return bool(re.match(pattern, email))

    async def post_users(
        self, user_credentials: Optional[UserCredentials] = None
    ) -> PostUsers201Response:
        """
        ユーザー登録の実装
        """
        if user_credentials is None:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="ユーザー情報が必要です",
            )

        if not isinstance(user_credentials.email, str):
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="メールアドレスは文字列である必要があります",
            )

        if not isinstance(user_credentials.password, str):
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="パスワードは文字列である必要があります",
            )

        if not self._validate_email(user_credentials.email):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="無効なメールアドレス形式です",
            )

        try:
            user_id = await self._service.create_user(
                email=user_credentials.email, password=user_credentials.password
            )
            return PostUsers201Response(id=user_id)
        except ValueError as e:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
