from utils.db import get_query_results
from models.word_select import WordSelect
LESSONS_TYPES = [

] 

WORDS_SO_FAR = set()
WORD_SO_FAR_IN_SENTENCES = set()


def create_lesson(word, idx):
    # TODO: load sentences translation and options with the word in them 
    return {}



def load_words(path):
    words = []
    with open(path) as f:
        lines = f.readlines()
        for l in lines:
            feilds = l.split('\t')
            w = WordSelect(
                    lang = f[0],
                    word = f[1],
                    pos = f[2],
                    min_wcount = f[3],
                    max_wcount = f[4],
                    sentences_count = f[5],
                    root_count= f[6])
            words.append(w)
    lessons = []
    i = 0
    for w in words:
        i+=1
        l = create_lesson(w,i)
        lessons.append(l)
    return lessons
    
        

