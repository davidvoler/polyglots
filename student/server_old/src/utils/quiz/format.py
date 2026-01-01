import random
from models.quiz import Quiz, Sentence, Option
from models.modes import PracticeMode


def prepare_quiz_sentence(s:dict,lang:str, to_lang:str, reverse_mode:bool=False):
    if reverse_mode:
        options = s.get("options", [])
        correct = s.get("text", "")
        sentence = s.get("to_text", "")
    else:
        options = s.get("to_options", [])
        correct = s.get("to_text", "")
        sentence = s.get("text", "")
    if not options or not correct:
        return None
    random.shuffle(options)
    options = [Option(option=correct, correct=True)] + [Option(option=o, correct=False) for o in options[:3]]
    random.shuffle(options)
    rec = s.get("recording", "")
    if rec and rec != "{}" and len(rec) > 5:
        rec = f"{lang}/{rec}"
    else:
        rec = ""
    
    sentence_id = s.get("part_id", "")
    sentence_id = s.get("dialogue_line", "")
    dialogue_id = s.get("dialogue_id", "")
    sentence_id=str(s.get("part_id", ""))
    words = s.get("words", [])
    if not words:
        words = []
    sentence = Sentence(
        sentence=sentence,
        options=options,
        sound=rec,
        sentence_id=sentence_id,
        dialogue_id=s.get("dialogue_id", ""),
        dialogue_line=s.get("dialogue_line", ""),
        words=words,
    )
    return sentence


def format_quiz(lang:str, to_lang:str, docs: list,mode:PracticeMode, reverse_mode:bool=False ) -> Quiz:
    quiz = Quiz(
        lang=lang, 
        to_lang=to_lang,
        mode=mode, 
    )
    sentences = []
    for doc in docs:
        s = prepare_quiz_sentence(doc, lang, to_lang, reverse_mode)
        if s:
            sentences.append(s)
    quiz.sentences = sentences
    return quiz



