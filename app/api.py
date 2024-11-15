from requests import request, RequestException
from typing import Any, Dict

from django.conf import settings


class APIClient:
    def __init__(self, base_url: str | None = None, headers: dict[str, str] | None = None, timeout: int = 10):
        self.base_url = base_url or settings.API_URL
        self.headers = headers if headers else {'Content-Type': "application/json"}
        self.timeout = timeout

    def _request(self, method: str, endpoint: str, params: dict[str, Any] | None = None, data: dict[str, Any] | None = None) -> dict[str, Any] | None:
        url = f"{self.base_url}/{endpoint}"
        try:
            response = request(
                method=method,
                url=url,
                headers=self.headers,
                params=params,
                json=data,
                timeout=self.timeout
            )
            response.raise_for_status()
            return response.json()
        except RequestException as e:
            print(f"Request failed: {e}")
            return None

    def get(self, endpoint: str, params: dict[str, Any] | None = None) -> dict[str, Any] | None:
        return self._request("GET", endpoint=endpoint, params=params)

    def post(self, endpoint: str, data: Dict[str, Any], params: Dict[str, Any] | None = None) -> dict[str, Any] | None:
        return self._request("POST", endpoint=endpoint, data=data, params=params)

    def put(self, endpoint: str, data: Dict[str, Any], params: Dict[str, Any] | None = None) -> dict[str, Any] | None:
        return self._request("PUT", endpoint=endpoint, data=data, params=params)

    def delete(self, endpoint: str, params: Dict[str, Any] | None = None) -> dict[str, Any] | None:
        return self._request("DELETE", endpoint=endpoint, params=params)
