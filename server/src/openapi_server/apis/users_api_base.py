# coding: utf-8

from typing import ClassVar, Dict, List, Tuple  # noqa: F401

from typing import Any, Optional
from openapi_server.models.post_users201_response import PostUsers201Response
from openapi_server.models.user_credentials import UserCredentials


class BaseUsersApi:
    subclasses: ClassVar[Tuple] = ()

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        BaseUsersApi.subclasses = BaseUsersApi.subclasses + (cls,)
    async def post_users(
        self,
        user_credentials: Optional[UserCredentials],
    ) -> PostUsers201Response:
        """ユーザーを登録する。"""
        ...
