import bcrypt
from typing import Optional
from openapi_server.repositories.user_repository import IUserRepository


class UserService:
    def __init__(self, user_repository: IUserRepository):
        self._repository = user_repository

    async def create_user(self, email: str, password: str) -> int:
        # メールアドレスの重複チェック
        existing_user = await self._repository.find_by_email(email)
        if existing_user:
            raise ValueError("このメールアドレスは既に登録されています")

        # パスワードのハッシュ化
        password_hash = bcrypt.hashpw(
            password.encode("utf-8"), bcrypt.gensalt()
        ).decode("utf-8")

        # ユーザーの作成
        return await self._repository.create(email, password_hash)
