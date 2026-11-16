"""Small HTTP client: bounded requests, JSON payloads, no automatic write retries."""
import logging
from urllib.parse import urlparse

import requests

log = logging.getLogger(__name__)


class ApiClient:
    def __init__(self, base_url, timeout=10):
        parsed = urlparse(base_url)
        if parsed.scheme not in {"http", "https"} or not parsed.netloc:
            raise ValueError("base_url must be an absolute HTTP(S) URL")
        if timeout <= 0:
            raise ValueError("timeout must be positive")
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({"Accept": "application/json"})

    def request(self, method, path, *, json=None):
        if not path.startswith("/") or path.startswith("//"):
            raise ValueError("path must start with a single slash")
        response = self.session.request(
            method, self.base_url + path, json=json, timeout=self.timeout
        )
        # Payloads, credentials and response bodies are deliberately not logged.
        log.info("%s %s -> %s (%.3fs)", method, path,
                 response.status_code, response.elapsed.total_seconds())
        return response

    def close(self):
        self.session.close()
