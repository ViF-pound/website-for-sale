from fastapi import APIRouter, Depends, HTTPException

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.app_auth.auth_shema import RegisterUser, LoginUser, UpdateData, ShowUser, ShowUserWithToken
from src.models.user_model import User
from src.db import get_session
from src.app_auth.auth_utils.utils import hach_password, check_hached_password, create_access_token
from src.get_current_user import get_current_user


auth_router = APIRouter(prefix="/auth", tags=["auth"])


@auth_router.post("/register", response_model=ShowUserWithToken)
async def register(data_user: RegisterUser, session:AsyncSession = Depends(get_session)):

    user = await session.scalar(select(User).where(User.email == data_user.email))
    if user:
        raise HTTPException(status_code=400, detail={"this email busy"})
    
    user = await session.scalar(select(User).where(User.user_name == data_user.user_name))
    if user:
        raise HTTPException(status_code=400, detail={"this name busy"})
    
    data_profile = data_user.model_dump()
    data_profile["password"] = await hach_password(password=data_user.password)

    user = User(**data_profile)
    session.add(user)
    await session.flush()

    user_id = user.id

    await session.commit()

    user_token = await create_access_token(user_id)
    data_profile["token"] = user_token

    return data_profile


@auth_router.post("/login")
async def login_user(data_user: LoginUser, session:AsyncSession = Depends(get_session)):

    if data_user.email: 

        user = await session.scalar(select(User).where(User.email == data_user.email))

        if check_hached_password(data_user.password, user.password):

            user_token = await create_access_token(user_id=user.id)
            return {"token": user_token}

        raise HTTPException(status_code=400, detail={"check enter data"})
    
    elif data_user.user_name:

        user = await session.scalar(select(User).where(User.user_name == data_user.user_name))

        if await check_hached_password(data_user.password, user.password) == user.password:
            
            user_token = await create_access_token(user_id=user.id)
            return {"token": user_token}

        raise HTTPException(status_code=400, detail={"check enter data"})
    
    raise HTTPException(status_code=400, detail={"no data"})
    

@auth_router.get("/profile", response_model=ShowUser)
async def show_profile(profile = Depends(get_current_user)):
    
    return profile


@auth_router.put("/update", response_model=ShowUser)
async def update_data_user(new_data_user: UpdateData, profile: User = Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    
    if new_data_user.new_user_name:
        profile.profile_name = new_data_user.new_profile_name

    if new_data_user.new_profile_name:
        if await check_hached_password(new_data_user.password, profile.password):
            profile.user_name = new_data_user.new_user_name
        else:
            raise HTTPException(status_code=400, detail={"check enter password"})

    if new_data_user.new_password:
        if await check_hached_password(new_data_user.password, profile.password):
            profile.password = await hach_password(new_data_user.new_password)
        else:
            raise HTTPException(status_code=400, detail={"check enter password"})

    await session.commit()
    await session.refresh(profile)

    return profile


@auth_router.get("/users")
async def get_all_users(session: AsyncSession = Depends(get_session)):
    
    result = await session.execute(select(User))
    users = result.scalars().all()

    return users