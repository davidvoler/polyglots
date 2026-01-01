import unittest
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from utils.results import *
from utils.stats import *
from models.results import Results
from models.user_vocab import UserVocab

results = Results(
        user_id='test_user',
        lang='el',
        part_id='like',
        dialogue_id='',
        dialogue_line='',
        step='200',
        attempts=1
        )



class TestExample(unittest.IsolatedAsyncioTestCase):
        
    async def test_async_function(self):
        global results
        for i in range(30):
            await save_results(results)

   

if __name__ == '__main__':
    unittest.main()