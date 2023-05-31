from datetime import date

from pydantic import BaseModel, EmailStr, Field


class ClientModel(BaseModel):
    firstname: str = Field("Ivan", min_length=2, max_length=20)
    lastname: str = Field("Ivanov", min_length=2, max_length=30)
    email: EmailStr
    phone_number: str = Field("0501112233", min_length=9, max_length=20)
    birthday: date = Field("1990-08-19")
    additional_data: str


class ClientResponse(BaseModel):
    id: int = 1
    firstname: str
    lastname: str
    email: EmailStr

    class Config:
        orm_mode = True


class BirthdayResponse(BaseModel):
    firstname: str
    lastname: str
    birthday: str
    email: EmailStr

    class Config:
        orm_mode = True


class UserModel(BaseModel):
    username: str = Field(min_length=5, max_length=16)
    email: EmailStr
    password: str = Field(min_length=6, max_length=10)


class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    avatar: str

    class Config:
        orm_mode = True


class TokenModel(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RequestEmail(BaseModel):
    email: EmailStr


class ChangePassword(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6, max_length=10)
    new_password: str = Field(min_length=6, max_length=10)
