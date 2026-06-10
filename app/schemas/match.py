from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel

from app.schemas.team import TeamResponse

class MatchCreate(BaseModel):
    round: str
    match_date: datetime
    group_name: str | None = None
    ground: str
    team1_id: UUID
    team2_id: UUID


class MatchUpdate(BaseModel):
    match_id: UUID
    round: str
    group_name: str | None = None
    ground: str
    score_team1: int
    score_team2: int
    team1_id: UUID
    team2_id: UUID
    finish: bool


class MatchResponse(BaseModel):
    match_id: UUID
    round: str
    match_date: datetime
    group_name: str | None
    ground: str
    time: str
    finish: bool
    team1_id: Optional[UUID] = None
    team2_id: Optional[UUID] = None

    team1: TeamResponse | None = None
    team2: TeamResponse | None = None

    score_team1: int
    score_team2: int

    class Config:
        from_attributes = True
