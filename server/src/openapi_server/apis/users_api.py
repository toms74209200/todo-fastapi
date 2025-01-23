# coding: utf-8

from typing import Dict, List  # noqa: F401
import importlib
import pkgutil

from openapi_server.apis.users_api_base import BaseUsersApi
import openapi_server.impl

from fastapi import (  # noqa: F401
    APIRouter,
    Body,
    Cookie,
    Depends,
    Form,
    Header,
    HTTPException,
    Path,
    Query,
    Response,
    Security,
    status,
)

from openapi_server.models.extra_models import TokenModel  # noqa: F401
from typing import Any, Optional
from openapi_server.models.post_users201_response import PostUsers201Response
from openapi_server.models.user_credentials import UserCredentials


router = APIRouter()

ns_pkg = openapi_server.impl
for _, name, _ in pkgutil.iter_modules(ns_pkg.__path__, ns_pkg.__name__ + "."):
    importlib.import_module(name)


@router.post(
    "/users",
    responses={
        201: {"model": PostUsers201Response, "description": "新しいユーザーが作成されました"},
        400: {"description": "Bad Request"},
    },
    tags=["users"],
    summary="ユーザー登録API",
    response_model_by_alias=True,
)
async def post_users(
    user_credentials: Optional[UserCredentials] = Body(None, description=""),
) -> PostUsers201Response:
    """ユーザーを登録する。"""
    if not BaseUsersApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseUsersApi.subclasses[0]().post_users(user_credentials)
