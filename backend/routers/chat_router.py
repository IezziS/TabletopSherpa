from fastapi import APIRouter
from backend.controllers.chat_controller import handle_ask
from backend.models import AskRequest, AskResponse


router = APIRouter()


#ask requests
@router.post("/ask", response_model=AskResponse)
def ask(body: AskRequest):
    return handle_ask(body)