from datetime import datetime
from uuid import UUID

from pydantic import BaseModel


class MatchCreate(BaseModel):
    round: str
    match_date: datetime
    group_name: str | None = None
    ground: str
    team1_id: UUID
    team2_id: UUID
    
class MatchUpdate(BaseModel):
    round: str
    group_name: str | None = None
    ground: str
    score_team1: int
    score_team2: int
    
class MatchResponse(BaseModel):
    match_id: UUID
    round: str
    match_date: datetime
    group_name: str | None
    ground: str

    team1_id: UUID
    team2_id: UUID

    score_team1: int
    score_team2: int

    class Config:
        from_attributes = True