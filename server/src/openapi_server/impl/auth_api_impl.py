from typing import Optional
from fastapi import HTTPException, status

from openapi_server.apis.auth_api_base import BaseAuthApi
from openapi_server.models.token import Token
from openapi_server.models.user_credentials import UserCredentials
from openapi_server.repositories.user_repository import InMemoryUserRepository
from openapi_server.services.auth_service import AuthService


class AuthApiImpl(BaseAuthApi):
    _instance = None
    _repository = None
    _service = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AuthApiImpl, cls).__new__(cls)
            cls._repository = InMemoryUserRepository()
            cls._service = AuthService(cls._repository)
        return cls._instance

    def __init__(self):
        # シングルトンなので初期化は__new__で行う
        pass

    async def post_auth(
        self, user_credentials: Optional[UserCredentials] = None
    ) -> Token:
        """
        ユーザー認証の実装
        """
        if user_credentials is None:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="認証情報が必要です",
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

        token = await self._service.authenticate_user(
            email=user_credentials.email, password=user_credentials.password
        )

        if token is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="認証に失敗しました",
            )

        return Token(token=token)
