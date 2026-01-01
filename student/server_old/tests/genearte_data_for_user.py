import unittest
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))
import random
from models.modes import PracticeMode
from models.quiz import QuizRequest, Quiz, Sentence
from utils.quiz.get_quiz import * 
from utils.results import *
from models.results import Results
from models.user_vocab import UserVocab

async def save_quiz_results(quiz: Quiz):
    for s in quiz.sentences:
        attempts = 1
        if random.randint(0, 10) > 7:
            attempts = 2
        results = Results(
            user_id='ebd27953d70f',
            lang=quiz.lang,
            part_id=s.sentence_id,
            dialogue_id=s.dialogue_id,
            dialogue_line=s.dialogue_line,
            step=quiz.practice_id,
            attempts=attempts
        )
        await save_results(results, test_mode=True)


class TestGetQuiz(unittest.IsolatedAsyncioTestCase):
    
    async def test_lines_dialogue(self):
        for i in range(2,350):
            for j in range(1, 3):
                qr = QuizRequest(
                    user_id='test_user',
                    lang='el',
                    to_lang='en',
                    last_mode=PracticeMode.dialogue_lines,
                    practice_type='step',
                    practice_id=str(i),
                    practice_mark=0.9,
                    practice_times=30
                )
                quiz = await get_quiz(qr)
                # print(quiz.mode)
                print(quiz.practice_id)
                # print(quiz.practice_times)
                # print(quiz.practice_mark)
                # print(quiz)
                await save_quiz_results(quiz)
                qr = QuizRequest(
                    user_id='ebd27953d70f',
                    lang='el',
                    to_lang='en',
                    last_mode=PracticeMode.step,
                    practice_type='step',
                    practice_id=str(i),
                    practice_mark=0.9,
                    practice_times=30
                )
                quiz = await get_quiz(qr)
                # print(quiz.mode)
                print(quiz.practice_id)
                # print(quiz.practice_times)
                # print(quiz.practice_mark)
                # print(quiz)
                await save_quiz_results(quiz)
            
if __name__ == '__main__':
    unittest.main()