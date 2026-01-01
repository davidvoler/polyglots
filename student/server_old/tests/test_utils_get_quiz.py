import unittest
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from models.modes import PracticeMode
from models.quiz import QuizRequest
from utils.quiz.get_quiz import * 




class TestGetQuiz(unittest.IsolatedAsyncioTestCase):
    # async def test_lines_structure(self):
    #     qr = QuizRequest(
    #     user_id='test_user',
    #     lang='en',
    #     to_lang='es',
    #     last_mode=PracticeMode.structure,
    #     practice_id='20',
    #     practice_type='step',
    #     practice_mark=0.1,
    #     practice_times=80
    #     )
    #     res = await get_quiz(qr)
    #     # print(res)
    #     print(res.mode, res.practice_id)
    #     # print(type(res))
    #     # for r in res.sentences:
    #     #     print(r)

    # async def test_lines_lines(self):
    #     qr = QuizRequest(
    #         user_id='test_user',
    #         lang='en',
    #         to_lang='es',
    #         last_mode=PracticeMode.dialogue_lines,
    #         practice_id='59',
    #         practice_type='step',
    #         practice_mark=0.5,
    #         practice_times=30
    #     )
    #     res = await get_quiz(qr)
    #     # print(res)
    #     print(res.mode)
    #     # print(type(res))
    #     # for r in res.sentences:
    #     #     print(r)

    # async def test_lines_step(self):
    #     qr = QuizRequest(
    #         user_id='test_user',
    #         lang='en',
    #         to_lang='es',
    #         last_mode=PracticeMode.step,
    #         practice_id='54',
    #         practice_type='step',
    #         practice_mark=0.5,
    #         practice_times=30
    #     )
    #     res = await get_quiz(qr)
    #     # print(res)
    #     print(res.mode)
    #     # print(type(res))
    #     # print(type(res))
    #     # for r in res.sentences:
    #     #     print(r)
    async def test_lines_dialogue(self):
        qr = QuizRequest(
            user_id='test_user',
            lang='el',
            to_lang='en',
            last_mode=PracticeMode.step,
            practice_id='200',
            practice_type='step',
            practice_mark=0.9,
            practice_times=30
        )
        quiz = await get_quiz(qr)
        # assert(res.mode == PracticeMode.dialogue)
        # print(res)
        # print(type(res))
        print(quiz.mode)
        print(quiz.practice_id)
        print(quiz.practice_times)
        print(quiz.practice_mark)
        # for r in res.sentences:
        #     print(r)
if __name__ == '__main__':
    unittest.main()