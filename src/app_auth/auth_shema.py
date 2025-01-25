import datetime

from pydantic import BaseModel, EmailStr, field_validator

class RegisterUser(BaseModel):

    name: str
    email: EmailStr
    dob: datetime.time
    password: str

    @field_validator("password")
    def Check_Length_Password(cls, password):
        if len(password) < 8:
            raise ValueError("password is less than 8 characters long")

class LoginUserEmail(BaseModel):

    email: EmailStr
    password: str

class LoginUserName(BaseModel):

    name: str
    password: str