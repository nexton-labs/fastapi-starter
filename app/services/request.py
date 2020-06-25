import datetime

import httpx


def default_headers() -> dict:
    return {
        "user-agent": "fastapi-base/0.0.1",
        "content-type": "application/json",
        "date": (
            datetime.datetime.utcnow()
            .replace(tzinfo=datetime.timezone.utc)
            .strftime("%a, %d %b %Y %H:%M:%S %Z")
        ),
    }


def http_client() -> httpx.Client:
    return httpx.Client(headers=default_headers())
