"""Auth routes — login / me."""

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel

from db import get_session
from db.queries import get_user_by_username, get_user_by_id, create_user
from services.auth import create_token, verify_password, hash_password
from routes._deps import current_user

router = APIRouter(prefix="/api/auth", tags=["auth"])


class LoginBody(BaseModel):
    username: str
    password: str


class RegisterBody(BaseModel):
    username: str
    password: str
    real_name: str


class LoginResponse(BaseModel):
    token: str
    username: str
    role: str
    real_name: str


@router.post("/login", response_model=LoginResponse)
def login(body: LoginBody):
    db = get_session()
    user = get_user_by_username(db, body.username)
    if user is None or not verify_password(body.password, user.password_hash):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="wrong credentials")

    token = create_token(user.id, user.username, user.role_id)
    return LoginResponse(
        token=token,
        username=user.username,
        role="admin" if user.role_id == 1 else "waiter",
        real_name=user.real_name,
    )


@router.post("/register")
def register(body: RegisterBody):
    db = get_session()
    try:
        user_id = create_user(db, body.username, body.password, role_id=2, real_name=body.real_name)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    token = create_token(user_id, body.username, 2)
    return LoginResponse(
        token=token,
        username=body.username,
        role="waiter",
        real_name=body.real_name,
    )


@router.get("/me")
def me(user=Depends(current_user)):
    db = get_session()
    u = get_user_by_id(db, int(user["sub"]))
    return {
        "id": u.id,
        "username": u.username,
        "real_name": u.real_name,
        "role": "admin" if u.role_id == 1 else "waiter",
    }
