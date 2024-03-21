import pytest
from clients.endpoints.post_req import PostReq


@pytest.fixture(scope="session")
def post_api():
    """Клиент для работы с API."""
    return PostReq()
