import unittest
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from utils.stats import *


s_req = StatsRequest(
        user_id='test_user',
        lang='en',
        step='1',
        granularity='day',

    )


class TestExample(unittest.IsolatedAsyncioTestCase):
        

    async def test_stats(self):
        global s_req
        print(await get_stats(s_req))
        s_req.granularity = 'week'
        print(await get_stats(s_req))
        s_req.granularity = 'hour'
        print(await get_stats(s_req))
        s_req.granularity = 'year'
        print(await get_stats(s_req))
        s_req.granularity = 'month'
        print(await get_stats(s_req))
        

    async def test_journal_stats(self):
        global s_req
        s = await get_journal_stats(s_req)
        #assert(s.granularity == 'week')

    async def test_mark(self):
        global s_req
        print(await get_mark(s_req))
    async def test_new_items(self):
        global s_req
        print(await get_new_items_stats(s_req))
    async def test_get_completed_items_stats(self):
        global s_req
        print(await get_completed_items_stats(s_req))
    async def test_full_stats(self):
        global s_req
        print(await full_stats(s_req))
    async def test_step_stats(self):
        print (await get_step_stats('test_user', 'en', '1'))
        


if __name__ == '__main__':
    unittest.main()