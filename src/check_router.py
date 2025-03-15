from fastapi import APIRouter, Depends
import datetime

from sqlalchemy import select
from src.models.user_model import User
from src.db import get_session
from src.app_auth.auth_utils.utils import hach_password
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/a", tags=["a"])

@router.post("/a")
async def password(password: str):
    return await hach_password(password)

@router.post("/b")
async def date():
    return datetime.date

@router.post("/s")
async def get_all_users(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(User))
    users = result.scalars().all()

    return users