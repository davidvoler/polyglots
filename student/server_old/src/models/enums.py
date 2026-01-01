from enum import Enum 

class ModeEnum(str, Enum):
    words=  'words' 
    level=  'level'
    refresh = 'refresh'   
    repeat=  'repeat' # repeat last quiz
    structure= 'structure'
    only_words = 'only_words'
    dialogue = 'dialogue' # Dialogue from start to end
    dialogue_lines = 'dialogue lines' # Dialogue lines - bu not in order 
   
    
    

class LevelEnum(str, Enum):
    novice=  'novice'
    beginner=  'beginner'
    intermediate=  'intermediate'
    advanced=  'advanced'
    expert=  'expert'
    evaluate = 'evaluate_level' # test like quiz that help us decide user level. 



class NumericLevelEnum(int, Enum):
    novice=1 # 'novice'
    beginner1=2 #  'beginner'
    beginner2=3 #  'beginner'
    intermediate1=4 #'intermediate'
    intermediate2=5 #'intermediate'
    intermediate3=6 #'intermediate'
    advanced1=7  #  'advanced'
    advanced2=8  #'advanced'
    advanced3=9 #  'advanced'
    expert=10 # 'expert'
    # evaluate = 'evaluate_level' # test like quiz that help us decide user level. 

class DialogueModeEnum(str, Enum):
    dialogue_preview = 'dialogue_preview' # Preview a dialogue from start to end 
    dialogue_line_mixed = 'dialogue_line_mixed' # Preview a dialogue from start to end 
    sentences = 'sentences' # sentences only
    words = 'words' # words only 
    sentence_words_mix = 'sentences_words_mix' # sentences and words mix
    sentence_their_words = 'sentence_their_words' # sentences and their words 
    refresh = 'refresh'   # refresh past sentences, words, lines  
    
class CurrentPracticeEnum(str, Enum):
    step = "step"
    dialogue = "dialogue"
    tag = "tag"