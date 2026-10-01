from dataclasses import dataclass
from typing import Annotated
from uuid import UUID

from fastapi import Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordBearer

from app.dependencies.db import DBSession
from app.core.security.jwt import decode_token
from app.modules.auth.models import User
from app.modules.auth.repositories import UserRepository

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/token")


@dataclass
class RequestMeta:
    ip: str
    user_agent: str | None


def get_request_user(request: Request) -> RequestMeta:
    ip = request.client.host if request.client else "unknown"
    user_agent = request.headers.get("user-agent")
    return RequestMeta(ip=ip, user_agent=user_agent)


UserContext = Annotated[RequestMeta, Depends(get_request_user)]

def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)], db: DBSession
) -> User:
    credentials_exc = HTTPException(
        status_code=401, detail="No Autorizado", headers={"WWW-Authenticate": "Bearer"}
    )
    try:
        payload = decode_token(token)
        user_id = UUID(payload.get("sub"))
    except Exception:
        raise credentials_exc

    repo = UserRepository(db)
    user = repo.get_by_id(user_id)

    if not user:
        raise credentials_exc

    return user


PlainCurrentUser = Annotated[User, Depends(get_current_user)]


@dataclass
class AuthenticatedUserContext:
    user: User
    ip: str
    user_agent: str | None

    @property
    def id(self):
        return self.user.id


def get_current_user_with_request(
    user: PlainCurrentUser, request_user: UserContext
) -> AuthenticatedUserContext:
    return AuthenticatedUserContext(
        user=user,
        ip=request_user.ip,
        user_agent=request_user.user_agent,
    )


# Use this when you need request metadata (audit IP/User-Agent).
CurrentUser = Annotated[AuthenticatedUserContext, Depends(get_current_user_with_request)]

# If you do not need audit metadata, use the following instead:
# CurrentUser = Annotated[User, Depends(get_current_user)]
