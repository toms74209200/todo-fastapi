import datetime
from locust import HttpUser, task, between

from lib.utils import random_string
from openapi_gen.openapi_client.api.auth_api import AuthApi
from openapi_gen.openapi_client.api.tasks_api import TasksApi
from openapi_gen.openapi_client.api.users_api import UsersApi
from openapi_gen.openapi_client.api_client import ApiClient
from openapi_gen.openapi_client.configuration import Configuration


class CreateUserAPI(HttpUser):
    """Test POST /users API"""

    wait_time = between(1, 5)

    @task
    def create_user(self):
        self.client.post(
            "/users",
            json={
                "email": f"{random_string(10)}@example.com",
                "password": random_string(10),
            },
        )


class AuthenticateAPI(HttpUser):
    """Test POST /auth API"""

    wait_time = between(1, 5)

    def on_start(self):
        # Create a user using OpenAPI client
        email = f"{random_string(10)}@example.com"
        self.password = random_string(10)
        api_client = ApiClient(Configuration(host=self.host))
        UsersApi(api_client).post_users(
            user_credentials={"email": email, "password": self.password}
        )
        self.email = email

    @task
    def authenticate_user(self):
        # Authenticate with locust client
        self.client.post(
            "/auth",
            json={
                "email": self.email,
                "password": self.password,
            },
        )


class CreateTaskAPI(HttpUser):
    """Test POST /tasks API"""

    wait_time = between(1, 5)

    def on_start(self):
        # Create user and get token using OpenAPI client
        email = f"{random_string(10)}@example.com"
        password = random_string(10)
        api_client = ApiClient(Configuration(host=self.host))
        UsersApi(api_client).post_users(
            user_credentials={"email": email, "password": password}
        )
        auth_response = AuthApi(api_client).post_auth(
            user_credentials={"email": email, "password": password}
        )
        self.token = auth_response.token
        self.headers = {"Authorization": f"Bearer {self.token}"}

    @task
    def create_task(self):
        deadline = datetime.datetime.now() + datetime.timedelta(days=1)
        self.client.post(
            "/tasks",
            headers=self.headers,
            json={
                "name": f"task_{random_string(5)}",
                "description": f"description_{random_string(10)}",
                "deadline": deadline.strftime("%Y-%m-%dT%H:%M:%SZ"),
                "completed": False,
            },
        )


class GetTasksAPI(HttpUser):
    """Test GET /tasks API"""

    wait_time = between(1, 5)

    def on_start(self):
        # Create user and get token using OpenAPI client
        email = f"{random_string(10)}@example.com"
        password = random_string(10)
        api_client = ApiClient(Configuration(host=self.host))
        self.user_response = UsersApi(api_client).post_users(
            user_credentials={"email": email, "password": password}
        )
        auth_response = AuthApi(api_client).post_auth(
            user_credentials={"email": email, "password": password}
        )
        self.token = auth_response.token
        self.headers = {"Authorization": f"Bearer {self.token}"}
        api_client.set_default_header("Authorization", f"Bearer {self.token}")
        tasks_api = TasksApi(api_client)
        deadline = datetime.datetime.now() + datetime.timedelta(days=1)
        tasks_api.post_tasks(
            post_tasks_request={
                "name": f"task_{random_string(5)}",
                "description": f"description_{random_string(10)}",
                "deadline": deadline.strftime("%Y-%m-%dT%H:%M:%SZ"),
                "completed": False,
            }
        )

    @task
    def get_tasks(self):
        self.client.get(
            f"/tasks?userId={self.user_response.id}",
            headers=self.headers,
        )


class UpdateTaskAPI(HttpUser):
    """Test PUT /tasks/{task_id} API"""

    wait_time = between(1, 5)

    def on_start(self):
        # Create user and get token using OpenAPI client
        email = f"{random_string(10)}@example.com"
        password = random_string(10)
        api_client = ApiClient(Configuration(host=self.host))
        UsersApi(api_client).post_users(
            user_credentials={"email": email, "password": password}
        )
        auth_response = AuthApi(api_client).post_auth(
            user_credentials={"email": email, "password": password}
        )
        self.token = auth_response.token
        self.headers = {"Authorization": f"Bearer {self.token}"}

        # Create a task to update using OpenAPI client
        api_client.set_default_header("Authorization", f"Bearer {self.token}")
        tasks_api = TasksApi(api_client)
        deadline = datetime.datetime.now() + datetime.timedelta(days=1)
        task_response = tasks_api.post_tasks(
            post_tasks_request={
                "name": f"task_{random_string(5)}",
                "description": f"description_{random_string(10)}",
                "deadline": deadline.strftime("%Y-%m-%dT%H:%M:%SZ"),
                "completed": False,
            }
        )
        self.task_id = task_response.id

    @task
    def update_task(self):
        self.client.put(
            f"/tasks/{self.task_id}",
            headers=self.headers,
            json={
                "name": f"updated_task_{random_string(5)}",
                "description": f"updated_description_{random_string(10)}",
                "deadline": (
                    datetime.datetime.now() + datetime.timedelta(days=2)
                ).strftime("%Y-%m-%dT%H:%M:%SZ"),
                "completed": True,
            },
        )


class DeleteTaskAPI(HttpUser):
    """Test DELETE /tasks/{task_id} API"""

    wait_time = between(1, 5)

    def on_start(self):
        # Create user and get token using OpenAPI client
        email = f"{random_string(10)}@example.com"
        password = random_string(10)
        api_client = ApiClient(Configuration(host=self.host))
        UsersApi(api_client).post_users(
            user_credentials={"email": email, "password": password}
        )
        auth_response = AuthApi(api_client).post_auth(
            user_credentials={"email": email, "password": password}
        )
        self.token = auth_response.token
        self.headers = {"Authorization": f"Bearer {self.token}"}

    def create_task(self):
        # Create a new task using OpenAPI client
        api_client = ApiClient(Configuration(host=self.host))
        api_client.set_default_header("Authorization", f"Bearer {self.token}")
        tasks_api = TasksApi(api_client)
        deadline = datetime.datetime.now() + datetime.timedelta(days=1)
        task_response = tasks_api.post_tasks(
            post_tasks_request={
                "name": f"task_{random_string(5)}",
                "description": f"description_{random_string(10)}",
                "deadline": deadline.strftime("%Y-%m-%dT%H:%M:%SZ"),
                "completed": False,
            }
        )
        return task_response.id

    @task
    def delete_task(self):
        # Create a task first using OpenAPI client
        task_id = self.create_task()
        # Then delete it with locust client
        self.client.delete(
            f"/tasks/{task_id}",
            headers=self.headers,
        )
