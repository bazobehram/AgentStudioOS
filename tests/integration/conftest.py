# pytest config for integration tests
import pytest
import os

@pytest.fixture
def db_url():
    """Database URL for integration tests"""
    return os.environ.get(
        'DATABASE_URL', 
        'postgresql://postgres:postgres@localhost:54322/postgres'
    )
