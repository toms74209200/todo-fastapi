# coding: utf-8

from typing import Dict, List  # noqa: F401
import importlib
import pkgutil

from openapi_server.apis.auth_api_base import BaseAuthApi
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
from openapi_server.models.token import Token
from openapi_server.models.user_credentials import UserCredentials


router = APIRouter()

ns_pkg = openapi_server.impl
for _, name, _ in pkgutil.iter_modules(ns_pkg.__path__, ns_pkg.__name__ + "."):
    importlib.import_module(name)


@router.post(
    "/auth",
    responses={
        200: {"model": Token, "description": "認証されたユーザーのトークンが返されます"},
        400: {"description": "Bad Request"},
    },
    tags=["auth"],
    summary="ユーザー認証API",
    response_model_by_alias=True,
)
async def post_auth(
    user_credentials: Optional[UserCredentials] = Body(None, description=""),
) -> Token:
    """ユーザー認証しトークンを取得する。"""
    if not BaseAuthApi.subclasses:
        raise HTTPException(status_code=500, detail="Not implemented")
    return await BaseAuthApi.subclasses[0]().post_auth(user_credentials)
