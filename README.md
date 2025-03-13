# todo-fastapi
TODO web app in Python/FastAPI and OpenAPI Generator

## Environments

- OpenAPI Generator 7.12.0
  - Node.js
  - Java
- Python 3.12.8
  - FastAPI 0.115.2

For web API testing

Web API automation test dependencies
- pytest 8.0.0

For development manual test dependencies
- JupyterLab 4.3.5

Load testing dependencies
- locust 2.32.6


You can set up the environments by using VSCode DevContainer.

## Usage

### Install OpenAPI Generator

```bash
$ npm install -g @openapitools/openapi-generator-cli
```

### Generate Python/FastAPI code from OpenAPI spec

The repository code will be overwritten if you run the following command, as this repository already contains generated code with customizations.

```bash
$ openapi-generator-cli generate -i https://raw.githubusercontent.com/toms74209200/openapi-todo-example/refs/heads/master/reference/spec.yaml -g python-fastapi -o ./server
```

### Launch Web API server

```bash
server$ PYTHONPATH=src uvicorn openapi_server.main:app --host 0.0.0.0 --port 8080
INFO:     Started server process [50323]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8080 (Press CTRL+C to quit)
```

### Test Web API

Generate Python code from OpenAPI spec.

```bash
e2etest$ openapi-generator-cli generate -i https://raw.githubusercontent.com/toms74209200/openapi-todo-example/refs/heads/master/reference/spec.yaml -g python -o openapi_gen
```

Install dependencies for testing.

```bash
test$ pip install -r requirements.txt
```

```bash
test/openapi_gen$ pip install -r requirements.txt
```

```bash
test/openapi_gen$ python setup.py install --user
```

Run tests.

```bash
test$ pytest tests/
```

### Launch JupyterLab for manual test

Generate Python code from OpenAPI spec, And install dependencies for manual testing as same as the above.

Install JupyterLab.

```bash
manualtest$ pip install -r requirements.txt
```

Launch JupyterLab. You can access JupyterLab from the URL shown in the log.

```bash
manualtest$ jupyter lab --ip 0.0.0.0 --NotebookApp.password=''
[I 2025-01-01 00:00:00.000 ServerApp] jupyterlab | extension was successfully loaded.
[I 2025-01-01 00:00:00.000 ServerApp] Registered jupyterlab_code_formatter server extension
[I 2025-01-01 00:00:00.000 ServerApp] jupyterlab_code_formatter | extension was successfully loaded.
[I 2025-01-01 00:00:00.000 ServerApp] Serving notebooks from local directory: /workspaces/todo-fastapi/
[I 2025-01-01 00:00:00.000 ServerApp] Jupyter Server 2.15.0 is running at:
[I 2025-01-01 00:00:00.000 ServerApp] http://8106ea164674:8888/lab?534d7a655b853b95ae86fd1700a0e7a52f
[I 2025-01-01 00:00:00.000 ServerApp]     http://127.0.0.1:8888/lab?534d7a655b853b95ae86fd1700a0e7a52f
[I 2025-01-01 00:00:00.000 ServerApp] Use Control-C to stop this server and shut down all kernels rmation).
[W 2025-01-01 00:00:00.000 ServerApp] No web browser found: Error('could not locate runnable browser').
[C 2025-01-01 00:00:00.000 ServerApp] 
    
    To access the server, open this file in a browser:
        file:///home/vscode/.local/share/jupyter/runtime/jpserver-1-open.html
    Or copy and paste one of these URLs:
        http://8106ea164674:8888/lab?token=7fd446f955585b534d7a655b853b95ae86fd1700a0e7a52f
        http://127.0.0.1:8888/lab?token=7fd446f955585b534d7a655b853b95ae86fd1700a0e7a52f
```

### Load testing

Generate Python code from OpenAPI spec, And install dependencies for load testing as same as the above.

Install locust.

```bash
loadtest$ pip install -r requirements.txt
```

Launch locust.

```bash
loadtest$ python -m locust -f locustfile.py --host=http://localhost:8080
[2025-01-01 00:00:00,000] 152d31b41ecf/INFO/locust.main: Starting Locust 2.32.6
[2025-01-01 00:00:00,000] 152d31b41ecf/INFO/locust.main: Starting web interface at http://0.0.0.0:8089
```

## License

[MIT License](LICENSE)

## Author

[toms74209200](<https://github.com/toms74209200>)
