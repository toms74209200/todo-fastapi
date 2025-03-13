#! /bin/bash

function setup_openapi_generator() {
    OPENAPI_GENERATOR_CLI_INSTALLED=$(openapi-generator-cli version >/dev/null 2>&1 && echo true || echo false)
    if [ "$OPENAPI_GENERATOR_CLI_INSTALLED" = true ]; then
        return
    fi

    sudo apt-get update
    sudo apt-get install -y openjdk-17-jdk nodejs npm
    npm install -g @openapitools/openapi-generator-cli
}

function setup_openapi_gen() {
    if [ -d openapi_gen ]; then
        return
    fi

    setup_openapi_generator
    openapi-generator-cli generate -i https://raw.githubusercontent.com/toms74209200/openapi-todo-example/refs/heads/master/reference/spec.yaml -g python -o openapi_gen
}

setup_openapi_gen

pip install -r requirements.txt
pip install -r openapi_gen/requirements.txt
pip install setuptools
cd openapi_gen && python setup.py install