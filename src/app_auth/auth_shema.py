import datetime

from pydantic import BaseModel, EmailStr


class RegisterUser(BaseModel):

    name: str
    email: EmailStr
    dob: datetime.time
    password: str


class LoginUserEmail(BaseModel):

    email: EmailStr
    password: str


class LoginUserName(BaseModel):

    user_name: str
    password: str


class UpdateDataName(BaseModel):

    new_profile_name: str
