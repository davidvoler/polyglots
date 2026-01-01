from utils.db import get_query_results, run_query
import json


async def get_exercise_details(exercise: dict):

   sql = """
   select l.text as sentence, l.elements, l.words,l.options,
   t.options as to_options, t.text as to_sentence
   from content_raw.sentence_elements l
   join content_raw.translation_links tl on l.lang = tl.lang and l.id = tl.id
   join content_raw.sentences t on tl.to_lang = t.lang and tl.to_id = t.id
   where tl.lang = %s and tl.to_lang = %s and tl.id = %s and tl.to_id = %s
   """
   results =await get_query_results(sql, (exercise['lang'], exercise['to_lang'], exercise.get("sentence_id",0), exercise.get("to_sentence_id",0)))
   if len(results)> 0 :
      exercise['sentence'] = results[0].get("sentence")
      exercise['elements'] = results[0]['elements']
      exercise['options'] = results[0]['options']
      exercise['to_sentence'] = results[0]['to_sentence']
      exercise['to_options'] = results[0]['to_options']
   return exercise


async def update_exercise_sentence(exercise:dict):
   updadate_sql = """
   update course.exercise set 
   sentence = %s,
   annotated_sentence = %s,
   options = %s,
   to_sentence = %s,
   to_options = %s,
   audio_link = %s
   where id = %s
   """
   print(exercise)
   await run_query(updadate_sql, (
      exercise.get("sentence"),
      json.dumps(exercise.get("elements")),
      exercise.get("options"),
      exercise.get("to_sentence"),
      exercise.get("to_options"),
      exercise.get("audio_link"),
      exercise.get("id"),
   ))


async def get_audio_link(sentence: str):
   sql = """
   select recording from content_raw.audio where lang = %s and id = %s
   order by audio_engine
   """
   results = await get_query_results(sql, (sentence['lang'], sentence['sentence_id']))
   try:
      return results[0]['recording']
   except:
      return ''

async def complete_exercise(lang: str, to_lang: str):
   sql = """
   select * from course.exercise
   where lang = %s and to_lang = %s and exercise_type in ('sentence', 'greeting') 
   """
   results = await get_query_results(sql, (lang, to_lang))
   for r in results:
      exercise = await get_exercise_details(r)
      audio_link = await get_audio_link(r)
      exercise['audio_link'] = audio_link
      await update_exercise_sentence(exercise)


