from uuid import UUID

from pydantic import BaseModel


class PredictionUpdate(BaseModel):
    score_team1: int
    score_team2: int


class GroupMatchPredictionResponse(BaseModel):
    username: str
    user_id: UUID

    score_team1: int
    score_team2: int


class PredictionCreate(BaseModel):
    match_id: UUID
    team1_id: UUID
    team2_id: UUID
    score_team1: int
    score_team2: int

class UserPredictionCreate(BaseModel):
    user_id: UUID
    group_id: UUID
    predictions: list[PredictionCreate]

class PredictionResponse(BaseModel):
    prediction_id: UUID
    match_id: UUID
    team1_id: UUID
    team2_id: UUID
    score_team1: int
    score_team2: int
    ended: bool

    class Config:
        from_attributes = True

class UserPredictionResponse(BaseModel):
    user_id: UUID
    group_id: UUID
    user_score: int

    predictions: list[PredictionResponse]


class UsersMatchPredictionResponse(BaseModel):
    user_id: UUID
    username: str
    score_team1: int | None
    score_team2: int | None
    first_name: str
    last_name: str
