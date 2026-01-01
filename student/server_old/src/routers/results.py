from fastapi import APIRouter, Depends
from models.results import Results
from utils.results import save_results
from utils.quiz_tatoeba.results import save_results as save_results_tatoeba
router = APIRouter()

@router.post("/save_results")
async def r_save_results(results: Results):
   print(results)
   if results.corpus == 'tatoeba':
      return await save_results_tatoeba(results)
   else:
      return await save_results(results)