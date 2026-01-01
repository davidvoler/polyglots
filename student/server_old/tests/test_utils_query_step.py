import unittest
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from models.user_vocab import UserVocab
from models.modes import PracticeMode
from utils.quiz.quiz_query_step import *

user_vocab = UserVocab(
        user_id='test_user',
        lang='en',
        to_lang='es',
        step='20'
)


class TestGetQuiz(unittest.IsolatedAsyncioTestCase):
    async def test_structure(self):
        global user_vocab
        user_vocab.last_mode = PracticeMode.structure
        res = await get_by_step(user_vocab)
        print(res)
    async def test_step(self):
        global user_vocab
        user_vocab.last_mode = PracticeMode.step
        res = await get_by_step(user_vocab)
        print(res)
    async def test_dialogue(self):
        global user_vocab
        user_vocab.last_mode = PracticeMode.dialogue
        res = await get_by_step(user_vocab)
        print(res)
    async def test_lines(self):
        global user_vocab
        user_vocab.last_mode = PracticeMode.dialogue_lines
        res = await get_by_step(user_vocab)
        print(res)


if __name__ == '__main__':
    unittest.main()