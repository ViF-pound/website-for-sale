import datetime

from pydantic import BaseModel, EmailStr


class RegisterUser(BaseModel):

    profile_name: str
    user_name: str
    email: EmailStr
    dob: datetime.date
    password: str


class LoginUser(BaseModel):

    email: EmailStr | None
    user_name: str | None
    password: str


class UpdateData(BaseModel):

    new_user_name: str | None
    new_profile_name: str | None
    password: str | None
    new_password: str | None


class ShowUserWithToken(BaseModel):

    profile_name: str
    user_name: str
    email: str
    dob: datetime.date
    token: str


class ShowUser(BaseModel):

    profile_name: str
    user_name: str
    email: str
    dob: datetime.date
