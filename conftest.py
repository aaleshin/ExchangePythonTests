import pytest


@pytest.fixture
def service_url():
    # host = "127.0.0.1"
    # port = "4000"
    # url = f'ws://{host}:{port}'
    url = 'ws://als.dedyn.io:4000'
    return url
