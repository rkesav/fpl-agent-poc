from pydantic import BaseModel, Field
from typing import List, Optional

class ChatRequest(BaseModel):
    message: str
    gw: Optional[int] = Field(default=None, description="Gameweek context")

class Suggestion(BaseModel):
    captain: str
    transfers_out: List[str]
    transfers_in: List[str]
    rationale: str

class ChatResponse(BaseModel):
    reply: str
    suggestion: Optional[Suggestion] = None