from datetime import datetime, timedelta
from typing import List

from sqlalchemy.orm import Session

from src.database.models import Client
from src.schemas import ClientModel


async def get_clients(limit: int, offset: int, db: Session):
    """
    The get_clients function returns a list of clients from the database.

    :param limit: int: Limit the number of clients returned
    :param offset: int: Determine how many clients to skip
    :param db: Session: Pass in the database session
    :return: A list of client objects
    """
    clients = db.query(Client).limit(limit).offset(offset).all()
    return clients


async def get_client(client_id: int, db: Session):
    """
    The get_client function returns a client object from the database.

    :param client_id: int: Specify the client id of the client we want to retrieve from our database
    :param db: Session: Pass the database session to the function
    :return: A client object
    """
    client = db.query(Client).filter_by(id=client_id).first()
    return client


async def get_client_by_email(email: str, db: Session):
    """
    The get_client_by_email function takes in an email and a database session,
    and returns the client with that email. If no such client exists, it returns None.

    :param email: str: Pass the email of the client to be retrieved from the database
    :param db: Session: Pass the database session to the function
    :return: The client object with the given email
    """
    client = db.query(Client).filter_by(email=email).first()
    return client


async def get_client_by_phone(phone_number: str, db: Session):
    """
    The get_client_by_phone function takes a phone number and returns the client associated with that phone number.

    :param phone_number: str: Filter the database query
    :param db: Session: Pass the database session to the function
    :return: A client object that matches the phone number provided
    """
    client = db.query(Client).filter_by(phone_number=phone_number).first()
    return client


async def create_client(body: ClientModel, db: Session):
    """
    The create_client function creates a new client in the database.

    :param body: ClientModel: Pass the data from the request body into a clientmodel object
    :param db: Session: Access the database
    :return: A client object
    """
    client = Client(**body.dict())
    db.add(client)
    db.commit()
    return client


async def update_client(body: ClientModel, user_id: int, db: Session):
    """
    The update_client function updates a client's information in the database.

    :param body: ClientModel: Pass the data from the request body to this function
    :param user_id: int: Get the client from the database
    :param db: Session: Access the database
    :return: A clientmodel object
    """
    client = await get_client(user_id, db)
    if client:
        client.firstname = body.firstname
        client.lastname = body.lastname
        client.email = body.email
        client.phone_number = body.phone_number
        client.birthday = body.birthday
        client.additional_data = body.additional_data
        db.add(client)
        db.commit()
    return client


async def remove_client(client_id: int, db: Session):
    """
    The remove_client function removes a client from the database.

    :param client_id: int: Specify the client to be removed
    :param db: Session: Pass the database session to the function
    :return: The client object that was deleted
    """
    client = await get_client(client_id, db)
    if client:
        db.delete(client)
        db.commit()
    return client


async def get_birthday(days: int, db: Session):
    """
    The get_birthday function takes in a number of days and a database session.
    It returns all clients whose birthday is within the next x days, where x is the number of days passed into the function.

    :param days: int: Specify the number of days to look ahead for birthdays
    :param db: Session: Pass the database session to the function
    :return: A list of clients with birthdays in the next x days
    """
    today = datetime.now().date()
    end_period = today + timedelta(days=days)
    client = db.query(Client).all()
    birthday_list = []
    for client in client:
        if type(client.birthday) == str:
            birthday_this_year = datetime.strptime(client.birthday, "%Y-%m-%d").date().replace(year=2023)
        else:
            birthday_this_year = client.birthday.replace(year=2023)
        if end_period >= birthday_this_year >= today:
            birthday_list.append(client)
    return birthday_list


async def search_clients(data: str, db: Session):
    """
    The search_clients function searches the database for clients that match a given string.
        The function takes in two parameters: data and db. Data is the string to be searched,
        and db is a Session object from SQLAlchemy.

    :param data: str: Search for a string in the database
    :param db: Session: Pass in the database session
    :return: A list of client objects
    """
    clients = db.query(Client).filter(Client.firstname.ilike(f"%{data}%") |
                                      Client.lastname.ilike(f"%{data}%") |
                                      Client.email.ilike(f"%{data}%")).all()
    return clients
