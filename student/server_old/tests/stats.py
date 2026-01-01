import unittest
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from utils.results import *
from utils.stats import *
from models.stats import Stats,StatsRequest




class TestExample(unittest.IsolatedAsyncioTestCase):
        

    async def test_stats(self):
        global user_vocab
        req = StatsRequest(
            user_id='test_user',
            lang='el',
            to_lang='en',
            granularity='year',
            customer_id='polyglots'
        )
        # res = await full_stats(req)
        # for k, v in dict(res).items():
        #     print(k)
        #     print(v)

        # print(await full_stats(req))
        # req.granularity = 'week'
        # print(await full_stats(req))
        # req.granularity = 'month'
        # print(await full_stats(req))
        # req.granularity = 'year'
        # print(await full_stats(req))
        # req.granularity = 'hour'
        # print(await full_stats(req))
        req.granularity = 'year'
        res = await single_query_stats(req)
        print(res)
        # print(len(res),'year')
        req.granularity = 'month'
        res = await single_query_stats(req)
        print(res)
        # print(len(res),'month')
        req.granularity = 'day'
        res = await single_query_stats(req)
        print(res)
        # print(len(res),'day')
        req.granularity = 'week_days'
        res = await single_query_stats(req)
        print(res)
        # print(len(res),'week_days')
        
  


if __name__ == '__main__':
    unittest.main()