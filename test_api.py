import pytest
import httpx
import tempfile
import os

url_api = "http://127.0.0.1:8000"

def test_api_running():
    response = httpx.get(f"{url_api}/purchases/")
    assert response.status_code == 200