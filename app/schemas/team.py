from uuid import UUID
from pydantic import BaseModel


class TeamCreate(BaseModel):
    country: str
    code: str
    flag: str


class TeamUpdate(BaseModel):
    country: str | None = None
    code: str | None = None
    flag: str | None = None


class TeamResponse(BaseModel):
    team_id: UUID
    country: str
    code: str
    flag: str
    external_id: int | None

    model_config = {
        "from_attributes": True
    }
