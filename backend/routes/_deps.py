"""Shared dependencies for route handlers."""

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from services.auth import verify_token

security = HTTPBearer()


def current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> dict:
    payload = verify_token(credentials.credentials)
    if payload is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="token invalid or expired")
    return payload


def admin_only(user: dict = Depends(current_user)) -> dict:
    if user.get("role") != 1:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="admin required")
    return user
