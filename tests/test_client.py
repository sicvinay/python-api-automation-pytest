from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from threading import Thread
from time import sleep

import pytest
import requests
from api.client import ApiClient


@pytest.mark.parametrize('url', ['relative/path', 'ftp://example.test'])
def test_invalid_base_url_is_rejected(url):
    with pytest.raises(ValueError, match='HTTP'):
        ApiClient(url)


def test_nonpositive_timeout_is_rejected():
    with pytest.raises(ValueError, match='positive'):
        ApiClient('http://127.0.0.1', timeout=0)


@pytest.mark.parametrize('path', ['students', '//example.test/students'])
def test_invalid_request_path_is_rejected(client, path):
    with pytest.raises(ValueError, match='single slash'):
        client.request('GET', path)


def test_request_to_stalled_server_times_out():
    class StalledHandler(BaseHTTPRequestHandler):
        def do_GET(self):
            sleep(0.25)

        def log_message(self, *args):
            pass

    server = ThreadingHTTPServer(('127.0.0.1', 0), StalledHandler)
    server.daemon_threads = True
    thread = Thread(target=server.serve_forever, daemon=True)
    thread.start()
    client = ApiClient(f'http://127.0.0.1:{server.server_port}', timeout=0.05)
    try:
        with pytest.raises(requests.exceptions.Timeout):
            client.request('GET', '/slow')
    finally:
        client.close()
        server.shutdown()
        server.server_close()
        thread.join(timeout=5)
