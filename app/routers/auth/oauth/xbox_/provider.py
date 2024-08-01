import httpx
from typing import Optional

__all__ = ("XBoxAuthEndpointProvider",)


class XBoxAuthEndpointProvider:

    def __init__(
        self,
        client_id: str,
        client_secret: str,
        redirect_uri: str,
        scopes: str,
    ):
        self._client_id: str = client_id
        self._client_secret: str = client_secret
        self._redirect_uri: str = redirect_uri
        self._scopes: str = scopes

    def generate_authorization_url(self, state: Optional[str] = None) -> str:
        query_params = {
            "client_id": self._client_id,
            "response_type": "code",
            "approval_prompt": "auto",
            "scope": self._scopes,
            "redirect_uri": self._redirect_uri,
        }

        if state:
            query_params["state"] = state

        return str(
            httpx.URL(
                "https://login.live.com/oauth20_authorize.srf", params=query_params
            )
        )
