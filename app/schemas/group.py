from pydantic import BaseModel
from uuid import UUID

class GroupCreate(BaseModel):
    name: str
    users_limit: int
    admin_id: str
    tournament_id: int
    description: str | None = None
    observations: str | None = None


class GroupResponse(BaseModel):
    group_id: UUID
    admin_id: UUID
    name: str
    users_limit: int
    invite_code: str
    description: str | None = None
    observations: str | None = None
    tournament_id: int

    class Config:
        from_attributes = True


class GroupMember(BaseModel):
    user_id: UUID
    group_id: UUID

    class Config:
        from_attributes = True


class GroupUserPositions(BaseModel):
    user_id: UUID
    username: str
    group_id: UUID
    email: str
    first_name: str
    last_name: str
    user_score: int | None = None

    class Config:
        from_attributes = True


class GroupJoin(BaseModel):
    invite_code: str
    user_id: UUID
