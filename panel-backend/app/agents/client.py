import httpx
import ssl
import time
import jwt
from typing import Any, Dict

from app.core.config import settings

class AgentClient:
    def __init__(self, base_url: str, node_id: str, *, mtls_cert: str | None = None, mtls_key: str | None = None, ca_cert: str | None = None):
        self.base_url = base_url.rstrip('/')
        self.node_id = node_id
        self.mtls_cert = (mtls_cert, mtls_key) if mtls_cert and mtls_key else None
        self.ca_cert = ca_cert

    def _jwt(self, action: str) -> str:
        now = int(time.time())
        payload = {
            "aud": self.node_id,
            "act": action,
            "iat": now,
            "exp": now + 300,
        }
        return jwt.encode(payload, settings.JWT_SIGNING_KEY, algorithm="HS256")

    def _client(self) -> httpx.Client:
        verify = self.ca_cert or True
        cert = self.mtls_cert
        return httpx.Client(verify=verify, cert=cert, timeout=30.0)

    def post(self, path: str, json: Dict[str, Any], action: str) -> httpx.Response:
        headers = {"Authorization": f"Bearer {self._jwt(action)}"}
        with self._client() as c:
            return c.post(f"{self.base_url}{path}", json=json, headers=headers)
