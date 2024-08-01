from fastapi import APIRouter

from pydantic import BaseModel, Field
from typing import Optional, List
from .xbox_ import XBoxAuthEndpointProvider, XboxProfile, XBoxLiveUser
from app.configs import oauthSettings
from app.services.auth.validate import read_jwt_payload
from app.types.auth.jwt import MicrosoftJWTPayload
from app.models.user.sso.microsoft import MircrosoftUserInfo, XboxUserInfo
from app.models.user.UserAuth import UserAuth
from app.utils.hash import gen_user_uuid
from app.utils.time import datetime_utc

router = APIRouter(prefix="/xbox", tags=["xbox"])


class CallbackPayload(BaseModel):
    code: str


xBoxAuthEndpointProvider = XBoxAuthEndpointProvider(
    client_id=oauthSettings.xbox.CLIENT_ID,
    client_secret=oauthSettings.xbox.CLIENT_SECRET,
    redirect_uri=oauthSettings.xbox.REDIRECT_URI,
    scopes=oauthSettings.xbox.SCOPES,
)


@router.get("/login")
async def auth_init():
    """Initialize auth and redirect"""
    url = xBoxAuthEndpointProvider.generate_authorization_url()

    return {"redirectTo": url}


@router.post("/callback")
async def auth_callback(payload: CallbackPayload):
    """Verify login"""
    user = XBoxLiveUser(authorization_code=payload.code)
    # NOTE: 나중에 정리되면 XBoxLiveUser에서 OAuth만 불러오고 사용자가
    # xbox 정보, 친구 목록 새로고침 요청할 때 받아서 갱신하면 됨
    # 로그인 되어 있는 동안 token_refresh는 프런트에서 알아서

    await user.init_user()

    _ms_token = read_jwt_payload(user.oauth2.id_token)
    ms_token = MicrosoftJWTPayload(**_ms_token)

    # 1. 이미 가입된 사용자인지 확인
    _user = await UserAuth.find_oauth_MS(uid=ms_token.uid, email=ms_token.email)
    if _user:
        _user.last_login = datetime_utc()
        await _user.save()
        return user.oauth2.model_dump(exclude=["user_id"])  # JWT

    # 2. 새로운 사용자의 경우 정보 저장 + Xbox 정보 가져와서 저장하기
    _xbox = XboxUserInfo(
        gamer_tag=user.xsts_token.gamertag,
        user_hash=user.xsts_token.userhash,
        xuid=user.xsts_token.xuid,
    )
    msUserInfo = MircrosoftUserInfo(uid=ms_token.uid, email=ms_token.email, xbox=_xbox)

    _user_id = gen_user_uuid(uid=ms_token.uid, email=ms_token.email)
    new_user = UserAuth(user_id=_user_id, oauth={"microsoft": msUserInfo})

    await new_user.insert()

    return user.oauth2.model_dump(exclude=["user_id"])  # JWT
