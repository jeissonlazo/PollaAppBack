from uuid import UUID
from pydantic import BaseModel


class TeamResponse(BaseModel):
    team_id: UUID
    country: str
    code: str
    flag: str

    model_config = {
        "from_attributes": True
    }