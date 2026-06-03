from uuid import UUID

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status

from sqlalchemy.orm import Session

from app.core.database import get_db

from app.schemas.match import (
    MatchCreate,
    MatchUpdate,
    MatchResponse
)

from app.services.match_service import (
    create_match,
    get_match_by_id,
    get_matches,
    get_matches_by_round,
    update_match,
    delete_match
)

router = APIRouter(
    prefix="/matches",
    tags=["Matches"]
)


@router.post(
    "",
    response_model=MatchResponse,
    status_code=status.HTTP_201_CREATED
)
def create_match_endpoint(
    match: MatchCreate,
    db: Session = Depends(get_db)
):
    return create_match(
        db=db,
        match_data=match
    )


@router.get(
    "",
    response_model=list[MatchResponse]
)
def get_matches_endpoint(
    round: str | None = None,
    db: Session = Depends(get_db)
):
    if round:
        return get_matches_by_round(
            db=db,
            round_name=round
        )

    return get_matches(db=db)


@router.get(
    "/{match_id}",
    response_model=MatchResponse
)
def get_match_endpoint(
    match_id: UUID,
    db: Session = Depends(get_db)
):
    match = get_match_by_id(
        db=db,
        match_id=match_id
    )

    if not match:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Match not found"
        )

    return match


@router.put(
    "/{match_id}",
    response_model=MatchResponse
)
def update_match_endpoint(
    match_id: UUID,
    match: MatchUpdate,
    db: Session = Depends(get_db)
):
    updated_match = update_match(
        db=db,
        match_id=match_id,
        match_data=match
    )

    if not updated_match:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Match not found"
        )

    return updated_match


@router.delete(
    "/{match_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_match_endpoint(
    match_id: UUID,
    db: Session = Depends(get_db)
):
    deleted = delete_match(
        db=db,
        match_id=match_id
    )

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Match not found"
        )

    return None