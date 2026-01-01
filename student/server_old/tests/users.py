import unittest
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from models.auth import *
from models.user_vocab import UserVocab
from utils.users import *


user_req = UserAuth0Request(
    email='tes5@test.com',
    full_name='Test User',
    sub='auth0|123456789'
)


user_vocab = UserVocab(
        user_id='test_user',
        lang='en',
        step='1'
    )


class TestUsers(unittest.IsolatedAsyncioTestCase):
    def test_simple_addition(self):
        
        self.assertEqual(1 + 1, 2)
        


    async def test_create_user(self):
        res = await get_or_create_user_by_auth_req(user_req)
        print(res, type(res))

    async def test_get_or_create_user_vocab(self):
        uv = UserVocab(
            user_id='c280d8dc6c34',
            lang='en',
            to_lang='es',
            step='1'
        )
        res = await get_or_create_user_vocab(uv.lang, uv.user_id, uv.customer_id)
        print(res, type(res))

    async def test_change_languages(self):
       
        user_id='2817e69efa0c'
        lang='fr'
        to_lang='es'
        customer_id='polyglots'
        res = await change_languages(user_id, lang, to_lang, customer_id)
        print(res, type(res))

    async def test_get_user_by_id(self):
       
        user_id='2817e69efa0c'
        res = await get_user_by_id(user_id)
        print(res, type(res))


    async def test_get_user_by_email_from_db(self):
       
        user_id='2817e69efa0c'
        res = await get_user_by_email_from_db('test@test.com')
        print(res, type(res))



if __name__ == '__main__':
    unittest.main()