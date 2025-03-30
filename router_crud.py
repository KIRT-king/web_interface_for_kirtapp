from typing import List, Optional
from fastapi import APIRouter, HTTPException

from pydantic_models import UserBase
from db import commands

router = APIRouter()


@router.get("/latest", response_model=List[UserBase])
def get_latest_users(limit: int = 10):
    return commands.get_latest_users_commands(limit)


@router.get("/search", response_model=List[UserBase])
def search_users(
    name: Optional[str] = None,
    phone_number: Optional[str] = None,
    email: Optional[str] = None,
):
    if not any([name, phone_number, email]):
        raise HTTPException(status_code=400, detail="At least one search parameter is required")

    users = commands.search_users_commands(name=name, phone_number=phone_number, email=email)

    if not users:
        raise HTTPException(status_code=404, detail="Users not found")

    return users
