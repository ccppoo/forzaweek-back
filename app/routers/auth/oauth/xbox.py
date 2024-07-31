from fastapi import APIRouter

from pydantic import BaseModel, Field
import httpx
from typing import Optional, List
from .xbox_ import XboxProfile, XBoxLiveUser
from app.configs import oauthSettings


router = APIRouter(prefix="/xbox", tags=["xbox"])


class CallbackPayload(BaseModel):
    code: str


class XBoxLiveManager:

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


xboxManager = XBoxLiveManager(
    client_id=oauthSettings.xbox.CLIENT_ID,
    client_secret=oauthSettings.xbox.CLIENT_SECRET,
    redirect_uri=oauthSettings.xbox.REDIRECT_URI,
    scopes=oauthSettings.xbox.SCOPES,
)


@router.get("/login")
async def auth_init():
    """Initialize auth and redirect"""
    url = xboxManager.generate_authorization_url()

    return {"redirectTo": url}


@router.post("/callback")
async def auth_callback(payload: CallbackPayload):
    """Verify login"""
    user = XBoxLiveUser(authorization_code=payload.code)
    # NOTE: 나중에 정리되면 XBoxLiveUser에서 OAuth만 불러오고 사용자가
    # xbox 정보, 친구 목록 새로고침 요청할 때 받아서 갱신하면 됨
    # 로그인 되어 있는 동안 token_refresh는 프런트에서 알아서
    from pprint import pprint

    await user.init_user()
    # print("로그인 성공")
    return user.oauth2.model_dump(exclude=["user_id"])  # JWT
