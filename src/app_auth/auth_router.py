import bcrypt

from fastapi import APIRouter, HTTPException

from sqlalchemy import select, selectinload

from src.app_auth.auth_shema import RegisterUser, LoginUserEmail, LoginUserName
from src.app_auth.auth_models import User
from src.db import session


auth_router = APIRouter(prefix="/auth", tags=["/auth"])


@auth_router.post("/register")
async def register(data_user: RegisterUser):

    hashed_password = bcrypt.hashpw(data_user.password.encode('utf-8'), bcrypt.gensalt())

    new_user = User(name = data_user.name, email = data_user.email, dob = data_user.dob, password = hashed_password)

    session.add(new_user)
    session.commit()

    return {"message": "user created successfully"}


@auth_router.post("/login/email")
async def loginUserEmail(data_user: LoginUserEmail):

    user = await session.scalars(select(User).where(User.email == data_user.email))

    if bcrypt.hashpw(data_user.password.encode('utf-8'), user.password) == user.password:
        return {"message": "successful authorization"}
    
    user = None

    raise HTTPException(status_code=404, detail="check enter data")


@auth_router.post("/login/name")
async def loginUserEmail(data_user: LoginUserName):

    user = await session.scalars(select(User).where(User.user_name == data_user.user_name))

    if bcrypt.hashpw(data_user.password.encode('utf-8'), user.password) == user.password:
        return {"message": "successful authorization"}
    
    user = None

    raise HTTPException(status_code=404, detail="check enter data")

@auth_router.get("/show/profile")
async def showProfile():
    
    if user == None:
