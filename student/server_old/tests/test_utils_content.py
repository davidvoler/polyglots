import unittest
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from utils.content import *
from models.preview import PreviewRequest

req = PreviewRequest(
        user_id='test_user',
        lang='en',
        to_lang='fr',

    )


class TestExample(unittest.IsolatedAsyncioTestCase):
        

    async def test_stats(self):
        global req
        print(await get_mixed(req))
       

if __name__ == '__main__':
    unittest.main()