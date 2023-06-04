from typing import List

from fastapi import APIRouter, HTTPException, status, Path, Query, Depends
from sqlalchemy.orm import Session

from src.database.db import get_db
from src.database.models import Client, User, Role
from src.schemas import ClientResponse, ClientModel, BirthdayResponse
from src.repository import clients as repository_clients
from src.services.auth import auth_service
from src.services.roles import RolesAccess
from fastapi_limiter.depends import RateLimiter

router = APIRouter(prefix="/clients", tags=["Clients"])

access_get = RolesAccess([Role.admin, Role.moderator, Role.user])
access_create = RolesAccess([Role.admin, Role.moderator])
access_update = RolesAccess([Role.admin, Role.moderator])
access_delete = RolesAccess([Role.admin])


@router.get("/", response_model=List[ClientResponse],
            dependencies=[Depends(access_get), Depends(RateLimiter(times=3, seconds=10))],
            description="No more than 3 requests per 10 seconds")
async def get_clients(limit: int = Query(10, le=300), offset: int = 0, db: Session = Depends(get_db),
                      _: User = Depends(auth_service.get_current_user)):
    """
    The get_clients function returns a list of clients.

    :param limit: int: Limit the number of clients returned
    :param le: Limit the number of clients that can be returned at once
    :param offset: int: Specify the number of records to skip before starting to return rows
    :param db: Session: Pass the database session to the repository layer
    :param _: User: Get the current user from the database
    :return: A list of clients
    """
    users = await repository_clients.get_clients(limit, offset, db)
    return users


@router.get("/birthday/", response_model=List[BirthdayResponse],
            dependencies=[Depends(access_get), Depends(RateLimiter(times=3, seconds=10))],
            description="No more than 3 requests per 10 seconds")
async def get_users_birthday(days: int = Query(7, le=365), db: Session = Depends(get_db),
                             _: User = Depends(auth_service.get_current_user)):
    """
    The get_users_birthday function returns a list of users whose birthday is within the next x days.

    :param days: int: Get the number of days from today to search for birthdays
    :param le: Limit the number of days to 365
    :param db: Session: Pass the database session to the function
    :param _: User: Tell fastapi that we want to use the auth_service
    :return: A list of users whose birthday is in the next x days
    """
    users = await repository_clients.get_birthday(days, db)
    if users is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Client not found")
    return users


@router.get("/search/", response_model=List[ClientResponse],
            dependencies=[Depends(access_get), Depends(RateLimiter(times=3, seconds=10))],
            description="No more than 3 requests per 10 seconds")
async def search_clients(data: str, db: Session = Depends(get_db), _: User = Depends(auth_service.get_current_user)):
    """
    The search_clients function searches for clients in the database.
        Args:
            data (str): The search term to be used when searching for clients.
            db (Session, optional): SQLAlchemy Session. Defaults to Depends(get_db).

    :param data: str: Search for a client by name or surname
    :param db: Session: Get the database session
    :param _: User: Check if the user is logged in
    :return: A list of clients
    """
    clients = await repository_clients.search_clients(data, db)
    if clients is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Client not found")
    return clients


@router.get("/{client_id}", response_model=ClientResponse,
            dependencies=[Depends(access_get), Depends(RateLimiter(times=3, seconds=10))],
            description="No more than 3 requests per 10 seconds")
async def get_user(client_id: int = Path(ge=1), db: Session = Depends(get_db),
                   _: User = Depends(auth_service.get_current_user)):
    """
    The get_user function is a GET request that returns the client with the given ID.
    The function requires an authenticated user and will return a 404 error if no client exists with the given ID.

    :param client_id: int: Specify the client id that is passed in the url
    :param db: Session: Pass the database session to the repository function
    :param _: User: Get the current user from the auth_service
    :return: A client object
    """
    client = await repository_clients.get_client(client_id, db)
    if client is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Client not found")
    return client


@router.post("/", response_model=ClientResponse, status_code=status.HTTP_201_CREATED,
             dependencies=[Depends(access_create),  Depends(RateLimiter(times=2, seconds=60))],
             description="No more than 2 requests per minute")
async def create_users(body: ClientModel, db: Session = Depends(get_db),
                       _: User = Depends(auth_service.get_current_user)):
    """
    The create_users function creates a new user in the database.
        It takes an email, password, and phone number as input parameters.
        The function returns the newly created user object.

    :param body: ClientModel: Get the data from the request body
    :param db: Session: Get the database session
    :param _: User: Check if the user is logged in,
    :return: A clientmodel object
    """
    client = await repository_clients.get_client_by_email(body.email, db)
    if client:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Client with this email already exist")
    client = await repository_clients.get_client_by_phone(body.phone_number, db)
    if client:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Client with this phone already exist")
    client = await repository_clients.create_client(body, db)
    return client


@router.put("/{client_id}", response_model=ClientResponse,
            dependencies=[Depends(access_update), Depends(RateLimiter(times=3, seconds=10))],
            description="No more than 3 requests per 10 seconds")
async def update_user(body: ClientModel, client_id: int = Path(ge=1), db: Session = Depends(get_db),
                      _: User = Depends(auth_service.get_current_user)):
    """
    The update_user function updates a user in the database.
        The function takes an id, which is used to find the user in question, and a body of data that contains all of the
        information that will be updated. If no client with this id exists, then an HTTPException is raised.

    :param body: ClientModel: Pass the client data to the function
    :param client_id: int: Specify the id of the client to be deleted
    :param db: Session: Get the database session
    :param _: User: Validate the user's token
    :return: The updated user object
    """
    client = await repository_clients.update_client(body, client_id, db)
    if client is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Client not found")
    return client


@router.delete("/{client_id}", response_model=ClientResponse,
               dependencies=[Depends(access_delete), Depends(RateLimiter(times=3, seconds=10))],
               description="No more than 3 requests per 10 seconds")
async def remove_user(client_id: int = Path(ge=1), db: Session = Depends(get_db),
                      _: User = Depends(auth_service.get_current_user)):
    """
    The remove_user function is used to remove a user from the database.
        The function takes in an integer client_id, which is the id of the client that will be removed.
        It also takes in a Session object db, which represents our database session and allows us to interact with it.
        Finally, it takes in an optional User object _ (which we don't use), but this parameter depends on another function called auth_service.get_current_user().

    :param client_id: int: Specify the client to be removed
    :param db: Session: Access the database
    :param _: User: Get the current user
    :return: A client object
    """
    client = await repository_clients.remove_client(client_id, db)
    if client is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Client not found")
    return client
