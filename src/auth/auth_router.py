from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from ..get_current_me import get_current_user
from ..db import get_session

from .auth_schema import RegisterUser, LoginUser, ShowUser, ShowUserWithToken, UpdateUser
from .auth_utils.utils import decode_password, check_password, create_access_token
from .auth_models import User

auth_router = APIRouter(prefix="/auth", tags=["auth"])

@auth_router.get("/profile", response_model=ShowUser)
async def profile(profile = Depends(get_current_user)):
     return profile

@auth_router.post("/login")
async def login_user(data:LoginUser, session:AsyncSession = Depends(get_session)):
    user = await session.scalar(select(User).where(User.email == data.email))

    if user:
        if await check_password(password=data.password, old_password=user.password):
            user_token = await create_access_token(user_id=user.id)
            return {"token":user_token}

    raise HTTPException(status_code=401, detail="user is not exists")

@auth_router.post("/register", response_model=ShowUserWithToken)
async def register_user(data:RegisterUser, session:AsyncSession = Depends(get_session)):
    data_dict = data.model_dump()
    
    data_dict["password"] = await decode_password(password=data.password)
    
    user = User(**data_dict)
    session.add(user) 
    await session.flush()

    user_id = user.id
    await session.commit()
        
    user_token = await create_access_token(user_id=user_id)
    data_dict["token"] = user_token  
    return data_dict

@auth_router.put("/update", response_model=ShowUser)
async def update_user(data:UpdateUser, profile:User = Depends(get_current_user), session:AsyncSession = Depends(get_session)):
    await session.refresh(profile)

    if data.email:
        profile.email = data.email
    if data.name:
        profile.name = data.name
    if data.surname:
        profile.surname = data.surname    
    if data.password:
        profile.password = await decode_password(password=data.password)

    await session.commit()
    await session.refresh(profile)

    return profile