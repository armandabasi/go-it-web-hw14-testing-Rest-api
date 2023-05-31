import enum
from datetime import date
from sqlalchemy import Column, Integer, String, DateTime, func, Date, Enum, Boolean
from sqlalchemy.orm import declarative_base, validates
from fastapi import HTTPException, status

Base = declarative_base()


class Role(enum.Enum):
    admin: str = 'admin'
    moderator: str = 'moderator'
    user: str = 'user'


class Client(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, index=True)
    firstname = Column(String)
    lastname = Column(String)
    email = Column(String, unique=True, index=True)
    phone_number = Column(String, unique=True)
    birthday = Column(Date)
    additional_data = Column(String)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

    @validates('phone_number')
    def validate_phone_number(self, key, phone_number):
        new_phone_number = (
            phone_number.strip()
            .removeprefix("+")
            .replace("(", "")
            .replace(")", "")
            .replace("-", "")
            .replace(" ", "")
        )
        if new_phone_number.isdigit():
            if len(new_phone_number) == 12:
                return "+" + new_phone_number
            elif len(new_phone_number) == 10 and new_phone_number.startswith("0"):
                return "+38" + new_phone_number
            elif len(new_phone_number) == 11 and new_phone_number.startswith("8"):
                return "+3" + new_phone_number
            else:
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid phone number format")


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String(50))
    email = Column(String(250), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    avatar = Column(String(255), nullable=True)
    refresh_token = Column(String(255), nullable=True)
    role = Column('role', Enum(Role), default=Role.user)
    confirmed = Column(Boolean, default=False)
