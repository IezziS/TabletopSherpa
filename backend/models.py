from pydantic import BaseModel
from typing import Optional


class AskRequest(BaseModel):
    question: str
    game: str
    edition: str
    history: Optional[list] = []
    
class AskResponse(BaseModel):
    answer: str
    retrieved : bool