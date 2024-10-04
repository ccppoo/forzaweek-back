from pydantic import BaseModel, Field, model_validator
from typing import Optional, List, ClassVar
from xbox.webapi.common.exceptions import AuthenticationException
import aiohttp
from pprint import pprint
from .profile import XboxProfile
from xbox.webapi.api.provider.profile.models import ProfileSettings
from datetime import datetime, timedelta, timezone
from xbox.webapi.authentication.models import (
    XAUResponse,
    XSTSResponse,
)
from app.configs import oauthSettings
from app.services.auth.validate import read_jwt_payload


def utc_now():
    return datetime.now(timezone.utc)


class OAuth2TokenResponse(BaseModel):
    token_type: str  # bearer
    expires_in: int  # 3600 -> MS가 알아서
    scope: str  # "XboxLive.signin XboxLive.offline_access"
    id_token: str  # JWT, 프런트가 관리할 것, user_id 포함된 것
    access_token: str
    refresh_token: Optional[str] = None
    user_id: str  # 이거는 id_token(jwt)에 있는건데 백에서는 편의를 위해서 미리 추출
    issued: datetime = Field(default_factory=utc_now)

    @model_validator(mode="before")
    @classmethod
    def extract_jwt_values(cls, data):
        _jwt = data["id_token"]
        jwt = read_jwt_payload(_jwt)
        if jwt is None:
            # TODO:  exception handling
            print("jwt 유효 ㄴㄴ")
            return

        return {**data, "user_id": jwt["sub"]}

    def is_valid(self) -> bool:
        return (self.issued + timedelta(seconds=self.expires_in)) > utc_now()


class Setting(BaseModel):
    id: str
    value: str


class ProfileUser(BaseModel):
    id: str
    hostId: str
    settings: List[Setting]
    isSponsoredUser: bool

    @property
    def GameDisplayName(self) -> str | None:

        return self._getSettings("GameDisplayName")

    @property
    def PublicGamerpic(self) -> str | None:
        return self._getSettings("PublicGamerpic")

    @property
    def PreferredColor(self) -> str | None:
        return self._getSettings("PreferredColor")

    def _getSettings(self, name: str) -> str | None:
        for setting in self.settings:
            if setting.id == name:
                return setting.value
        return None


class ProfileResponse(BaseModel):
    profileUsers: List[ProfileUser]


class XBoxLiveUser:

    SCOPE: ClassVar[str] = oauthSettings.xbox.SCOPES
    REDIRECT_URI: ClassVar[str] = oauthSettings.xbox.REDIRECT_URI

    authorization_code: Optional[str] = Field(default=None)
    # 아래는 나중에 초기화
    oauth2: Optional[OAuth2TokenResponse] = Field(default=None)
    # Xbox-Achievement-Unlocker => 이게 있어야 XBox API로 접근 가능
    user_token: Optional[XAUResponse] = Field(default=None)  #
    # XSTS, gatekeeper for Xbox LIVE. Xbox Live Authentication Token
    xsts_token: Optional[XSTSResponse] = Field(default=None)

    def __init__(self, authorization_code: str) -> None:
        self.authorization_code = authorization_code

    async def init_user(self) -> None:
        await self.request_tokens()

    @property
    def xuid(self) -> str:
        """
        Gets the Xbox User ID

        Returns: Xbox user Id
        """
        return self.xsts_token.xuid

    async def request_tokens(self) -> None:
        """Request all tokens."""

        self.oauth2 = await self.request_oauth_token()
        self.xbox_user_token = await self.request_xbox_user_token()
        self.xsts_token = await self.request_xsts_token()

    async def request_oauth_token(self) -> OAuth2TokenResponse:
        """Request OAuth2 token."""
        return await self._oauth2_token_request(
            {
                "grant_type": "authorization_code",
                "code": self.authorization_code,
                "scope": XBoxLiveUser.SCOPE,
                "response_type": "id_token",
                "redirect_uri": XBoxLiveUser.REDIRECT_URI,
            }
        )

    # 로그인 이후 oauth_token refresh는 클라이언트 쪽이 요청보내면 해주고 반환해주기
    async def refresh_oauth_token(
        self,
    ) -> OAuth2TokenResponse:
        """Refresh OAuth2 token."""
        return await self._oauth2_token_request(
            {
                "grant_type": "refresh_token",
                "scope": XBoxLiveUser.SCOPE,
                "refresh_token": self.oauth2.refresh_token,
            }
        )

    async def _oauth2_token_request(self, data: dict) -> OAuth2TokenResponse:
        """Execute token requests."""

        data["client_id"] = oauthSettings.xbox.CLIENT_ID
        data["client_secret"] = oauthSettings.xbox.CLIENT_SECRET
        headers = {"content-type": "application/x-www-form-urlencoded"}
        # print()
        # pprint(f"params로 추가하는거 {data}")
        # print()
        # HOST = "https://login.live.com/oauth20_token.srf?"
        # for k, v in data.items():
        #     HOST = f"{HOST}{k}={v}&"
        # print(f"{HOST=}")
        async with aiohttp.ClientSession() as session:
            async with session.post(
                "https://login.live.com/oauth20_token.srf",
                data=data,
                headers=headers,
            ) as response:
                _json = await response.json()
                # pprint(_json)
                return OAuth2TokenResponse(**_json)

    async def request_xbox_user_token(
        self,
        relying_party: str = "http://auth.xboxlive.com",
        use_compact_ticket: bool = False,
    ) -> XAUResponse:
        """Authenticate via access token and receive user token."""
        url = "https://user.auth.xboxlive.com/user/authenticate"
        headers = {"x-xbl-contract-version": "1"}
        data = {
            "RelyingParty": relying_party,
            "TokenType": "JWT",
            "Properties": {
                "AuthMethod": "RPS",
                "SiteName": "user.auth.xboxlive.com",
                "RpsTicket": (
                    self.oauth2.access_token
                    if use_compact_ticket
                    else f"d={self.oauth2.access_token}"
                ),
            },
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=data, headers=headers) as response:
                _json = await response.json()
                return XAUResponse(**_json)

    async def request_xsts_token(
        self, relying_party: str = "http://xboxlive.com"
    ) -> XSTSResponse:
        """Authorize via user token and receive final X token."""
        url = "https://xsts.auth.xboxlive.com/xsts/authorize"
        headers = {"x-xbl-contract-version": "1"}
        data = {
            "RelyingParty": relying_party,
            "TokenType": "JWT",
            "Properties": {
                "UserTokens": [self.xbox_user_token.token],
                "SandboxId": "RETAIL",
            },
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=data, headers=headers) as response:
                if response.status == 401:  # if unauthorized
                    # TODO:  exception handling
                    print(
                        "Failed to authorize you! Your password or username may be wrong or you are trying to use child account (< 18 years old)"
                    )
                    raise AuthenticationException()
                _json = await response.json()
                return XSTSResponse(**_json)

    async def get_profile(self) -> ProfileResponse:
        PROFILE_URL = "https://profile.xboxlive.com"
        url = PROFILE_URL + f"/users/xuid({self.xuid})/profile/settings"
        HEADERS_PROFILE = {
            "x-xbl-contract-version": "3",
            "Authorization": self.xsts_token.authorization_header_value,
        }
        SEPARATOR = ","

        params = {
            "settings": SEPARATOR.join(
                [
                    ProfileSettings.GAMERTAG,
                    ProfileSettings.MODERN_GAMERTAG,
                    ProfileSettings.MODERN_GAMERTAG_SUFFIX,
                    ProfileSettings.UNIQUE_MODERN_GAMERTAG,
                    ProfileSettings.REAL_NAME_OVERRIDE,
                    ProfileSettings.BIOGRAPHY,
                    ProfileSettings.LOCATION,
                    ProfileSettings.GAMERSCORE,
                    ProfileSettings.GAME_DISPLAYPIC_RAW,
                    ProfileSettings.TENURE_LEVEL,
                    ProfileSettings.ACCOUNT_TIER,
                    ProfileSettings.XBOX_ONE_REP,
                    ProfileSettings.PREFERRED_COLOR,
                    ProfileSettings.WATERMARKS,
                    ProfileSettings.IS_QUARANTINED,
                ]
            ),
        }

        async with aiohttp.ClientSession() as session:
            async with session.get(
                url, params=params, headers=HEADERS_PROFILE
            ) as response:
                _json = await response.json()
                return ProfileResponse(**_json)

    async def get_profile_min(self) -> ProfileUser:
        PROFILE_URL = "https://profile.xboxlive.com"
        url = PROFILE_URL + f"/users/xuid({self.xuid})/profile/settings"
        HEADERS_PROFILE = {
            "x-xbl-contract-version": "3",
            "Authorization": self.xsts_token.authorization_header_value,
        }
        SEPARATOR = ","

        params = {
            "settings": SEPARATOR.join(
                [
                    ProfileSettings.GAME_DISPLAY_NAME,
                    ProfileSettings.PUBLIC_GAMERPIC,
                    ProfileSettings.PREFERRED_COLOR,
                ]
            ),
        }

        async with aiohttp.ClientSession() as session:
            async with session.get(
                url, params=params, headers=HEADERS_PROFILE
            ) as response:
                _json = await response.json()
                return ProfileResponse(**_json).profileUsers[0]
