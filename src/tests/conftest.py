import pytest
from fastapi.testclient import TestClient

from app.api.routes import setup_routes
from app.service import app

setup_routes(app)
base_url: str = 'http://test/api/v1/'


@pytest.fixture(scope='session')
def test_client():
    setup_routes(app)
    with TestClient(app) as client:
        yield client
