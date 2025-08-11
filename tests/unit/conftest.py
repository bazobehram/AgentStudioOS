# pytest config for unit tests
import pytest

@pytest.fixture
def mock_env():
    """Mock environment variables for tests"""
    return {
        'SUPABASE_URL': 'http://localhost:54321',
        'SUPABASE_ANON_KEY': 'test-key'
    }
