import unittest
import sys
import os
from datetime import datetime, date
from dotenv import load_dotenv
from unittest.mock import MagicMock
from sqlalchemy.orm import Session
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
load_dotenv()
from src.database.models import UserLogin, User
from src.schemas import UserBase, UserUpdate
from src.repository.users import (get_users, get_user, create_user, remove_user, update_user, get_birthday)

class TestUsers(unittest.IsolatedAsyncioTestCase):

    def setUp(self):
        self.session = MagicMock(spec=Session)
        self.user = UserLogin(id=1)

    async def test_get_users(self):
        users = [User(), User(), User()]
        self.session.query().filter().all.return_value = users
        result = await get_users(db=self.session, user_login=self.user)
        self.assertEqual(result, users)

    async def test_get_users_not_found(self):
        self.session.query().filter().all.return_value = None
        result = await get_users(db=self.session, user_login=self.user)
        self.assertIsNone(result)

    async def test_get_user_found(self):
        user = User()
        self.session.query().filter().first.return_value = user
        result = await get_user(user_id=1, user_login=self.user, db=self.session)
        self.assertEqual(result, user)

    async def test_get_user_not_found(self):
        self.session.query().filter().first.return_value = None
        result = await get_user(user_id=1, user_login=self.user, db=self.session)
        self.assertIsNone(result)

    async def test_create_user(self):
        body = UserBase(first_name='Jack', last_name='Browny', email='jack1@example.com',
                        phone='+380964334566', birthday=date.today(), data='info')
        result = await create_user(body=body, user_login=self.user, db=self.session)
        self.assertEqual(result.first_name, body.first_name)
        self.assertEqual(result.last_name, body.last_name)
        self.assertEqual(result.email, body.email)
        self.assertEqual(result.phone, body.phone)
        self.assertEqual(result.birthday, body.birthday)
        self.assertEqual(result.data, body.data)
        self.assertTrue(hasattr(result, "id"))

    async def test_remove_user_found(self):
        user = User()
        self.session.query().filter().first.return_value = user
        result = await remove_user(user_id=1, user_login=self.user, db=self.session)
        self.assertEqual(result, user)

    async def test_remove_user_not_found(self):
        self.session.query().filter().first.return_value = None
        result = await remove_user(user_id=1, user_login=self.user, db=self.session)
        self.assertIsNone(result)

    async def test_update_user_found(self):
        body = UserUpdate(first_name='Harry', last_name='Potter', email='harry@example.com',
                        phone='+380964334561', birthday=date.today(), data='Gryffingor')
        user = User()
        self.session.query().filter().first.return_value = user
        result = await update_user(user_id=1, body=body, user_login=self.user, db=self.session)
        self.assertEqual(result, user)
    
    async def test_update_user_not_found(self):
        body = UserUpdate(first_name='Harry', last_name='Potter', email='harry@example.com',
                        phone='+380964334561', birthday=date.today(), data='Gryffingor')
        self.session.query().filter().first.return_value = None
        result = await update_user(user_id=1, body=body, user_login=self.user, db=self.session)
        self.assertIsNone(result)
    

if __name__ == '__main__':
    unittest.main()