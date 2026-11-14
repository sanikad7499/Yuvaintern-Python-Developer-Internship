import pytest
import app as greenlife_app


@pytest.fixture

def database_path(tmp_path, monkeypatch):
    """Use an isolated database for each test; never modify the real DB."""
    test_database = tmp_path / "test_greenlife.db"
    monkeypatch.setattr(greenlife_app, "DATABASE", str(test_database))
    greenlife_app.init_db()
    return test_database


@pytest.fixture

def client(database_path):
    greenlife_app.app.config.update(TESTING=True)
    with greenlife_app.app.test_client() as test_client:
        yield test_client
