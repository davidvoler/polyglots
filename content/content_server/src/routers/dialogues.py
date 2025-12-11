from fastapi import APIRouter
from models.dialogue import DialogueRequest, Dialogue

router = APIRouter()

@router.post("/", response_model=list[Dialogue])
async def list_dialogues(request: DialogueRequest):
    return []

    