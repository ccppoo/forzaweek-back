from app.models.user.UserAuth import UserAuth
from fastapi import Depends, HTTPException, status
from typing import Annotated
from fastapi.security import OAuth2PasswordBearer
from app.types.auth.jwt import MicrosoftJWTPayload
from app.exceptions.auth import InvalidAuthorizationToken
from .validate.xbox import read_jwt_payload

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]) -> UserAuth:
    # FUTURE: oauth 여러가지 있을 경우 헤더에 OAuth 제공자 값 하나 더 추가해서 여기서 식별하고
    # 어떤 validate 함수를 가져올지 결정

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = read_jwt_payload(token)
        msJWTPayload = MicrosoftJWTPayload(**payload)
    except InvalidAuthorizationToken:
        raise credentials_exception
    user = await UserAuth.find_oauth_MS(uid=msJWTPayload.uid, email=msJWTPayload.email)
    if user is None:
        raise credentials_exception
    return user


async def get_current_active_user(
    current_user: Annotated[UserAuth, Depends(get_current_user)],
) -> UserAuth:
    # NOTE: 나중에 밴, 등등 막을 때
    # if current_user.disabled:
    #     raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
