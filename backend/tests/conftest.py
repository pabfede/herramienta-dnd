import pytest
from fastapi.testclient import TestClient

from app.config import get_settings
from app.db import _engine_cache
from app.main import app


@pytest.fixture
def client(tmp_path, monkeypatch):
    monkeypatch.setenv("DND_DATA_DIR", str(tmp_path))
    get_settings.cache_clear()
    _engine_cache.clear()
    with TestClient(app) as test_client:
        yield test_client
    _engine_cache.clear()
    get_settings.cache_clear()
