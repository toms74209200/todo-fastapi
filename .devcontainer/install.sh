#!/bin/bash

WORKDIR=/workspaces/todo-fastapi

cd $WORKDIR

sudo pip install -r requirements.txt

sudo pip install -r /workspaces/todo-fastapi/server/requirements.txt
