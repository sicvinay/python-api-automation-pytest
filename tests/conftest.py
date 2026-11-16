import json
from pathlib import Path
from threading import Thread
import uuid

import pytest

from api.client import ApiClient
from api.students import StudentsApi
from tests.support.demo_api import DemoServer


def pytest_addoption(parser):
    parser.addoption("--base-url", default=None,
                     help="Optional disposable API implementing docs/API_CONTRACT.md")
    parser.addoption("--allow-external-writes", action="store_true",
                     help="Explicitly enable POST/PUT/DELETE against --base-url")


@pytest.fixture(scope="session")
def base_url(request):
    supplied = request.config.getoption("--base-url")
    if supplied:
        if not request.config.getoption("--allow-external-writes"):
            raise pytest.UsageError("--base-url requires --allow-external-writes; use a test environment")
        yield supplied
        return
    server = DemoServer()
    thread = Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        yield f"http://127.0.0.1:{server.server_port}"
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=5)


@pytest.fixture
def client(base_url):
    instance = ApiClient(base_url)
    try:
        yield instance
    finally:
        instance.close()


@pytest.fixture
def students(client):
    return StudentsApi(client)


@pytest.fixture
def student_payload():
    path = Path(__file__).resolve().parents[1] / "data" / "student.json"
    with path.open(encoding="utf-8") as stream:
        payload = json.load(stream)
    payload["first_name"] = "Demo-" + uuid.uuid4().hex[:10]
    return payload


@pytest.fixture
def create_student(students):
    created = []

    def create(payload):
        response = students.create(payload)
        assert response.status_code == 201, f"Creation failed: HTTP {response.status_code}"
        identifier = response.json()["data"]["id"]
        created.append(identifier)
        return response

    yield create
    for identifier in reversed(created):
        response = students.delete(identifier)
        assert response.status_code in (204, 404), f"Cleanup failed: HTTP {response.status_code}"


@pytest.fixture
def student_id(create_student, student_payload):
    return create_student(student_payload).json()["data"]["id"]
