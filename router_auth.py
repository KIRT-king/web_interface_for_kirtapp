import time

import bcrypt
from fastapi import APIRouter, Request, HTTPException, status, Response


from db import commands

router = APIRouter()

@router.post("/login")
def login(response: Response, username: str, password: str):
    user = commands.get_user_by_username(username)
    if not user or not bcrypt.checkpw(password.encode(), user.password.encode('utf-8')):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Invalid username or password",)
    session_id = commands.create_session(user.id)

    response.set_cookie(
        key="session_id",
        value=session_id,
        max_age=900,
        expires=int(time.time()) + 900,
        httponly=True,
        secure=False,
        samesite="Lax",
    )

    return {"message": "Logged in successfully"}

@router.get("/admin")
def admin_panel(request: Request):
    session_id = request.cookies.get("session_id")
    user = commands.get_user_by_session(session_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Forbidden",)

    return {"message": f"Welcome, {user.username}!"}

@router.post("/logout")
def logout(response: Response, request: Request):
    session_id = request.cookies.get("session_id")

    if session_id:
        commands.delete_session(session_id)

    response.delete_cookie("session_id")
    return {"message": "Logged out successfully"}