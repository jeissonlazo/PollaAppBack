from pydantic import BaseModel


class GroupCreate(BaseModel):
    name: str
    users_limit: int


class GroupResponse(BaseModel):
    group_id: str
    admin_id: str
    name: str
    users_limit: int
    invite_code: str

    class Config:
        from_attributes = True