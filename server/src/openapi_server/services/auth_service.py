import jwt
import bcrypt
import os
from datetime import datetime, timedelta, UTC
from typing import Optional

from openapi_server.repositories.user_repository import InMemoryUserRepository

# 環境変数から設定を読み込み、設定されていない場合はデフォルト値を使用
SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "your-secret-key")
ALGORITHM = os.environ.get("JWT_ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(
    os.environ.get("JWT_ACCESS_TOKEN_EXPIRE_MINUTES", "30")
)


class AuthService:
    def __init__(self, repository: InMemoryUserRepository):
        self._repository = repository

    async def authenticate_user(self, email: str, password: str) -> Optional[str]:
        user = await self._repository.find_by_email(email)
        if user is None:
            return None

        # パスワードの比較
        try:
            if not bcrypt.checkpw(
                password.encode("utf-8"), user["password_hash"].encode("utf-8")
            ):
                return None

        except Exception:
            return None

        # トークンの生成
        try:
            token_data = {
                "sub": str(user["id"]),
                "email": user["email"],
                "exp": datetime.now(UTC)
                + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
            }
            token = jwt.encode(token_data, SECRET_KEY, algorithm=ALGORITHM)
            return token
        except Exception:
            return None
