import logging
from libgravatar import Gravatar
from sqlalchemy.orm import Session

from src.database.models import User
from src.schemas import UserModel


async def get_user_by_email(email: str, db: Session) -> User | None:
    """
    The get_user_by_email function takes in an email and a database session,
    and returns the user associated with that email. If no such user exists, it returns None.

    :param email: str: Specify the type of parameter that is expected to be passed into the function
    :param db: Session: Pass the database session to the function
    :return: The first user that matches the email address passed in
    """
    return db.query(User).filter(User.email == email).first()


async def create_user(body: UserModel, db: Session) -> User:
    """
    The create_user function creates a new user in the database.

    :param body: UserModel: Get the user's email address
    :param db: Session: Connect to the database
    :return: A user object
    """
    avatar = None
    try:
        g = Gravatar(body.email)
        avatar = g.get_image()
    except Exception as e:
        logging.error(e)
    new_user = User(**body.dict(), avatar=avatar)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


async def update_token(user: User, token: str | None, db: Session) -> None:
    """
    The update_token function updates the refresh token for a user.

    :param user: User: Identify the user in the database
    :param token: str | None: Set the refresh_token field in the user table
    :param db: Session: Access the database
    :return: Nothing, so the type is none
    """
    user.refresh_token = token
    db.commit()


async def confirmed_email(email: str, db: Session) -> None:
    """
    The confirmed_email function takes in an email and a database session,
    and sets the confirmed field of the user with that email to True.


    :param email: str: Pass the email of the user who is trying to confirm their account
    :param db: Session: Pass in the database session
    :return: Nothing
    """
    user = await get_user_by_email(email, db)
    user.confirmed = True
    db.commit()


async def update_avatar(email, url: str, db: Session) -> User:
    """
    The update_avatar function updates the avatar of a user.

    :param email: Find the user in the database
    :param url: str: Specify the type of data that is being passed into the function
    :param db: Session: Pass in the database session
    :return: The updated user object
    """
    user = await get_user_by_email(email, db)
    user.avatar = url
    db.commit()
    return user


async def save_new_password(user: User, password: str, db: Session) -> None:
    """
    The save_new_password function takes a user object, a password string, and the database session.
    It then sets the user's password to be equal to the new password string.
    Finally it commits this change to the database.

    :param user: User: Pass the user object to the function
    :param password: str: Pass the new password to the function
    :param db: Session: Pass the database session to the function
    :return: None
    """
    user.password = password
    db.commit()
