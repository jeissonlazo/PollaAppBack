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
