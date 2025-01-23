#!/bin/bash

WORKDIR=/workspaces/todo-fastapi

cd $WORKDIR

pip install --user -r requirements.txt

npm install -g @openapitools/openapi-generator-cli

make openapi

pip install --user -r /workspaces/todo-fastapi/server/requirements.txt