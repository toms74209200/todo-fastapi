#! /bin/bash

function setup_openapi_generator() {
    if ! openapi-generator-cli version >/dev/null 2>&1; then
        OPENAPI_GENERATOR_CLI_INSTALLED=false
    fi
    if [ $OPENAPI_GENERATOR_CLI_INSTALLED ]; then
        return
    fi
    if ! java -version >/dev/null 2>&1; then
        JAVA_PACKAGE=openjdk-21-jdk
    fi
    if ! npm -v >/dev/null 2>&1; then
        NODE_PACKAGE="nodejs npm"
    fi

    sudo apt-get update
    sudo apt-get install -y $JAVA_PACKAGE $NODE_PACKAGE
    npm install -g @openapitools/openapi-generator-cli
}

function setup_openapi_gen() {
    if [ -d openapi_gen ]; then
        return
    fi
    openapi-generator-cli generate -i https://raw.githubusercontent.com/toms74209200/openapi-todo-example/refs/heads/master/reference/spec.yaml -g python -o openapi_gen
}

setup_openapi_generator
setup_openapi_gen

pip install -r requirements.txt
pip install -r openapi_gen/requirements.txt
pip install setuptools
cd openapi_gen && python setup.py install --user