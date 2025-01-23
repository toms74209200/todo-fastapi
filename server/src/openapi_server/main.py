# coding: utf-8

"""
    openapi-todo-example

    TODO application Web API example using by OpenAPI Specification

    The version of the OpenAPI document: 1.0.0
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


from fastapi import FastAPI

from openapi_server.apis.auth_api import router as AuthApiRouter
from openapi_server.apis.tasks_api import router as TasksApiRouter
from openapi_server.apis.users_api import router as UsersApiRouter

app = FastAPI(
    title="openapi-todo-example",
    description="TODO application Web API example using by OpenAPI Specification",
    version="1.0.0",
)

app.include_router(AuthApiRouter)
app.include_router(TasksApiRouter)
app.include_router(UsersApiRouter)
