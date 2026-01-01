from fastapi import APIRouter, Depends
from models.preview import PreviewRequest
from utils.content import get_mixed
from utils.users import get_user_by_id
router = APIRouter()


@router.post("/mixed")
async def r_get_quiz(req: PreviewRequest):
    # print('--------------------------------------')
    # print(req)
    if not req.lang or not req.to_lang:
        user = await get_user_by_id(req.user_id)
        req.lang = user.lang
        req.to_lang = user.to_lang
    # print('--------------------------------------')
    return await get_mixed(req)