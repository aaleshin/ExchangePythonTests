import pytest


@pytest.fixture
def service_url():
    host = "127.0.0.1"
    port = "4000"
    url = f'ws://{host}:{port}'
    return url
