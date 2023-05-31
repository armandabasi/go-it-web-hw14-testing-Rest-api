import unittest
from unittest.mock import MagicMock

1
from datetime import datetime, timedelta

from sqlalchemy.orm import Session

from src.database.models import Client, User
from src.repository.clients import (
    get_clients,
    get_client,
    get_client_by_email,
    get_client_by_phone,
    create_client,
    update_client,
    remove_client,
    get_birthday,
    search_clients

)
from src.schemas import ClientModel


class TestClients(unittest.IsolatedAsyncioTestCase):
    def setUp(self) -> None:
        self.session = MagicMock(spec=Session)
        self.user = User(id=1)

    async def test_get_clients(self):
        clients = [Client() for _ in range(5)]
        self.session.query(Client).limit().offset().all.return_value = clients
        result = await get_clients(10, 0, self.session)
        self.assertEqual(result, clients)

    async def test_get_client(self):
        client = Client()
        self.session.query(Client).filter_by().first.return_value = client
        result = await get_client(1, self.session)
        self.assertEqual(result, client)

    async def test_get_client_not_found(self):
        self.session.query(Client).filter_by().first.return_value = None
        result = await get_client(1, self.session)
        self.assertIsNone(result)

    async def test_get_client_by_email(self):
        email = "mark_twen@example.com"
        client = Client(email=email)
        self.session.query(Client).filter_by().first.return_value = client
        result = await get_client_by_email(email, self.session)
        self.assertEqual(result, client)

    async def test_get_client_by_email_not_found(self):
        email = "mark_twen@example.com"
        self.session.query(Client).filter_by().first.return_value = None
        result = await get_client_by_email(email, self.session)
        self.assertIsNone(result)

    async def test_get_client_by_phone_10_symbol(self):
        phone = "0931112233"
        client = Client(phone_number=phone)
        self.session.query(Client).filter_by().first.return_value = client
        result = await get_client_by_phone(phone, self.session)
        self.assertEqual(result, client)

    async def test_get_client_by_phone_12_symbol(self):
        phone = "380931112233"
        client = Client(phone_number=phone)
        self.session.query(Client).filter_by().first.return_value = client
        result = await get_client_by_phone(phone, self.session)
        self.assertEqual(result, client)

    async def test_get_client_by_phone_11_symbol(self):
        phone = "80931112233"
        client = Client(phone_number=phone)
        self.session.query(Client).filter_by().first.return_value = client
        result = await get_client_by_phone(phone, self.session)
        self.assertEqual(result, client)

    async def test_get_client_by_phone_not_found(self):
        phone = "0931112233"
        self.session.query(Client).filter_by().first.return_value = None
        result = await get_client_by_phone(phone, self.session)
        self.assertIsNone(result)

    async def test_create_client(self):
        body = ClientModel(firstname="Ivan",
                           lastname="Ivanov",
                           email="mark_twen@example.com",
                           phone_number="+380501112233",
                           birthday="1990-08-19",
                           additional_data="some text")
        result = await create_client(body, self.session)
        self.assertEqual(result.firstname, body.firstname)
        self.assertEqual(result.lastname, body.lastname)
        self.assertEqual(result.email, body.email)
        self.assertEqual(result.phone_number, body.phone_number)
        self.assertEqual(result.additional_data, body.additional_data)
        self.assertTrue(hasattr(result, "id"))

    async def test_update_client(self):
        client = Client()
        body = ClientModel(firstname="Ivan",
                           lastname="Ivanov",
                           email="mark_twen@example.com",
                           phone_number="+380501112233",
                           birthday="1990-08-19",
                           additional_data="some text")
        self.session.query(Client).filter_by().first.return_value = client
        self.session.commit.return_value = None
        result = await update_client(body, 1, self.session)
        self.assertEqual(result, client)

    async def test_update_client_not_found(self):
        body = ClientModel(firstname="Ivan",
                           lastname="Ivanov",
                           email="mark_twen@example.com",
                           phone_number="+380501112233",
                           birthday="1990-08-19",
                           additional_data="some text")
        self.session.query(Client).filter_by().first.return_value = None
        self.session.commit.return_value = None
        result = await update_client(body, 1, self.session)
        self.assertIsNone(result)

    async def test_remove_client(self):
        client = Client()
        self.session.query(Client).filter_by().first.return_value = client
        result = await remove_client(1, self.session)
        self.assertEqual(result, client)

    async def test_remove_client_not_found(self):
        self.session.query(Client).filter_by().first.return_value = None
        result = await remove_client(1, self.session)
        self.assertIsNone(result)

    async def test_get_birthday(self):
        clients = [
            Client(id=1, birthday="2000-06-02"),
            Client(id=2, birthday="2000-06-10"),
            Client(id=3, birthday="2000-06-15"),
        ]
        self.session.query().all.return_value = clients
        result = await get_birthday(7, self.session)
        self.assertEqual(len(result), 1)
        self.assertIn(clients[0], result)

    async def test_search_clients(self):
        clients = [
            Client(id=1, firstname="Pavlo"),
            Client(id=2, lastname="Pavlov"),
            Client(id=3, email="Pavlooo@example.com"),
        ]
        self.session.query(Client).filter().all.return_value = clients
        result = await search_clients("pav", self.session)

        self.assertEqual(len(result), 3)
        self.assertIn(clients[0], result)
        self.assertIn(clients[1], result)
        self.assertIn(clients[2], result)
