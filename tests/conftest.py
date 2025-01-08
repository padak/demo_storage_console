import pytest
from app import app as flask_app

@pytest.fixture
def app():
    yield flask_app

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def mock_keboola_token():
    return "test-token-123"

@pytest.fixture
def mock_keboola_endpoint():
    return "connection.keboola.com"

@pytest.fixture
def mock_headers(mock_keboola_token):
    return {'X-StorageApi-Token': mock_keboola_token} 