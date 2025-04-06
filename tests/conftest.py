import pytest
from fastapi.testclient import TestClient

from dashboard.api.main import app
from tests.test_utils import setup_test_device


@pytest.fixture(scope="session", autouse=True)
def setup_device_once():
    setup_test_device("Box 1")


@pytest.fixture(scope="module")
def client():
    return TestClient(app)
