from fastapi import APIRouter

from pydantic import BaseModel, Field
from typing import Optional, List
from .xbox_ import XBoxAuthEndpointProvider, XboxProfile, XBoxLiveUser
from .xbox_.user import OAuth2TokenResponse
from app.configs import oauthSettings
from app.services.auth.validate import read_jwt_payload
from app.types.auth.jwt import MicrosoftJWTPayload
from app.models.user.sso.microsoft import MircrosoftUserInfo, XboxUserInfo
from app.models.user.UserAuth import UserAuth
from app.utils.hash import gen_user_uuid
from app.utils.time import datetime_utc
import aiohttp

router = APIRouter(prefix="/xbox", tags=["xbox"])


class CallbackPayload(BaseModel):
    code: str


class RefreshTokenPayload(BaseModel):
    refreshToken: str


xBoxAuthEndpointProvider = XBoxAuthEndpointProvider(
    client_id=oauthSettings.xbox.CLIENT_ID,
    client_secret=oauthSettings.xbox.CLIENT_SECRET,
    redirect_uri=oauthSettings.xbox.REDIRECT_URI,
    scopes=oauthSettings.xbox.SCOPES,
)


async def _oauth2_token_request(refresh_token: str) -> OAuth2TokenResponse:
    """Execute token requests."""
    data = {
        "grant_type": "refresh_token",
        "scope": oauthSettings.xbox.SCOPES,
        "refresh_token": refresh_token,
        "client_id": oauthSettings.xbox.CLIENT_ID,
        "client_secret": oauthSettings.xbox.CLIENT_SECRET,
    }

    async with aiohttp.ClientSession() as session:
        async with session.post(
            "https://login.live.com/oauth20_token.srf", data=data
        ) as response:
            _json = await response.json()
            # pprint(_json)
            return OAuth2TokenResponse(**_json)


@router.get("/login")
async def auth_init():
    """Initialize auth and redirect"""
    url = xBoxAuthEndpointProvider.generate_authorization_url()

    return {"redirectTo": url}


@router.post("/refresh")
async def token_refresh(token: RefreshTokenPayload):
    """return new token"""
    print(token)

    new_token = await _oauth2_token_request(token.refreshToken)

    return new_token


@router.post("/callback")
async def auth_callback(payload: CallbackPayload):
    """Verify login"""
    user = XBoxLiveUser(authorization_code=payload.code)
    # NOTE: 나중에 정리되면 XBoxLiveUser에서 OAuth만 불러오고 사용자가
    # xbox 정보, 친구 목록 새로고침 요청할 때 받아서 갱신하면 됨
    # 로그인 되어 있는 동안 token_refresh는 프런트에서 알아서

    await user.init_user()

    # PUBLIC_GAMERPIC -> 사진
    # PREFERRED_COLOR -> 선호 색 (JSON)

    user_profile = await user.get_profile_min()

    _ms_token = read_jwt_payload(user.oauth2.id_token)
    ms_token = MicrosoftJWTPayload(**_ms_token)

    # 1. 이미 가입된 사용자인지 확인
    _user = await UserAuth.find_oauth_MS(uid=ms_token.uid, email=ms_token.email)
    if _user:
        _user.last_login = datetime_utc()
        _user.oauth.xbox.gamer_tag = user_profile.GameDisplayName
        _user.oauth.xbox.profile_image = user_profile.PublicGamerpic
        _user.oauth.xbox.preferred_color = user_profile.PreferredColor
        await _user.save()
        return user.oauth2.model_dump(exclude=["user_id"])  # JWT

    # 2. 새로운 사용자의 경우 정보 저장 + Xbox 정보 가져와서 저장하기
    msUserInfo = MircrosoftUserInfo(uid=ms_token.uid, email=ms_token.email)
    xboxUserInfo = XboxUserInfo(
        gamer_tag=user.xsts_token.gamertag,
        user_hash=user.xsts_token.userhash,
        xuid=user.xsts_token.xuid,
        profile_image=user_profile.PublicGamerpic,
        preferred_color=user_profile.PreferredColor,
    )
    _user_id = gen_user_uuid(uid=ms_token.uid, email=ms_token.email)
    new_user = UserAuth(
        user_id=_user_id, oauth={"microsoft": msUserInfo, "xbox": xboxUserInfo}
    )

    await new_user.insert()

    return user.oauth2.model_dump(exclude=["user_id"])  # JWT
