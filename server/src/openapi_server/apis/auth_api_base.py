# coding: utf-8

from typing import ClassVar, Dict, List, Tuple  # noqa: F401

from typing import Any, Optional
from openapi_server.models.token import Token
from openapi_server.models.user_credentials import UserCredentials


class BaseAuthApi:
    subclasses: ClassVar[Tuple] = ()

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        BaseAuthApi.subclasses = BaseAuthApi.subclasses + (cls,)
    async def post_auth(
        self,
        user_credentials: Optional[UserCredentials],
    ) -> Token:
        """ユーザー認証しトークンを取得する。"""
        ...
