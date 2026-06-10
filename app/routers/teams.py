from uuid import UUID

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status

from sqlalchemy.orm import Session

from app.core.database import get_db

from app.schemas.team import (
    TeamCreate,
    TeamUpdate,
    TeamResponse
)

from app.services.team_service import (
    create_team,
    get_teams,
    get_team_by_id,
    update_team,
    delete_team
)

router = APIRouter(
    prefix="/teams",
    tags=["Teams"]
)

from uuid import UUID

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status

from sqlalchemy.orm import Session

from app.core.database import get_db

from app.schemas.team import (
    TeamCreate,
    TeamUpdate,
    TeamResponse
)

from app.services.team_service import (
    create_team,
    get_teams,
    get_team_by_id,
    update_team,
    delete_team
)

router = APIRouter(
    prefix="/teams",
    tags=["Teams"]
)

@router.get(
    "",
    response_model=list[TeamResponse]
)
def get_teams_endpoint(
    db: Session = Depends(get_db)
):
    return get_teams(db)
  
  
@router.get(
    "/{team_id}",
    response_model=TeamResponse
)
def get_team_endpoint(
    team_id: UUID,
    db: Session = Depends(get_db)
):
    team = get_team_by_id(db, team_id)

    if not team:
        raise HTTPException(
            status_code=404,
            detail="Team not found"
        )

    return team
  
@router.put(
    "/{team_id}",
    response_model=TeamResponse
)
def update_team_endpoint(
    team_id: UUID,
    team: TeamUpdate,
    db: Session = Depends(get_db)
):
    updated_team = update_team(
        db=db,
        team_id=team_id,
        data=team.model_dump(exclude_unset=True)
    )

    if not updated_team:
        raise HTTPException(
            status_code=404,
            detail="Team not found"
        )

    return updated_team
  
@router.delete("/{team_id}")
def delete_team_endpoint(
    team_id: UUID,
    db: Session = Depends(get_db)
):
    team = delete_team(db, team_id)

    if not team:
        raise HTTPException(
            status_code=404,
            detail="Team not found"
        )

    return {"message": "Team deleted successfully"}