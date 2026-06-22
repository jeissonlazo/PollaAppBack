from uuid import UUID

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status

from sqlalchemy.orm import Session

from app.core.database import get_db

from app.schemas import prediction
from app.schemas.group import (
    GroupCreate,
    GroupJoin,
    GroupResponse,
    GroupMember,
    GroupUserPositions,
)

from app.services.group_service import (
    add_user_to_group_by_invite_code,
    create_group,
    get_group_by_id,
    get_group_members,
    update_group,
    delete_group,
    get_user_groups,
)

router = APIRouter(prefix="/groups", tags=["Groups"])


@router.post("", response_model=GroupResponse, status_code=status.HTTP_201_CREATED)
def create_group_endpoint(group: GroupCreate, db: Session = Depends(get_db)):
    return create_group(
        db=db,
        admin_id=group.admin_id,
        name=group.name,
        users_limit=group.users_limit,
        description=group.description,
        observations=group.observations,
        tournament_id=group.tournament_id,
    )


@router.get("/{group_id}", response_model=GroupResponse)
def get_group_endpoint(group_id: UUID, db: Session = Depends(get_db)):
    group = get_group_by_id(db=db, group_id=group_id)

    if not group:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Group not found"
        )

    return group


@router.put("/{group_id}", response_model=GroupResponse)
def update_group_endpoint(
    group_id: UUID, group: GroupCreate, db: Session = Depends(get_db)
):
    updated_group = update_group(
        db=db,
        group_id=group_id,
        name=group.name,
        users_limit=group.users_limit,
        admin_id=group.admin_id,
    )

    if not updated_group:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Group not found"
        )

    return updated_group


@router.post("/join", response_model=GroupMember)
def join_group(group_join: GroupJoin, db: Session = Depends(get_db)):
    member = add_user_to_group_by_invite_code(
        db=db, invite_code=group_join.invite_code, user_id=group_join.user_id
    )
    if not member:
        raise HTTPException(status_code=404, detail="Group not found")

    return member


@router.delete("/{group_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_group_endpoint(group_id: UUID, db: Session = Depends(get_db)):
    deleted = delete_group(db=db, group_id=group_id)

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Group not found"
        )

    return None


@router.get("/{user_id}/groups", response_model=list[GroupResponse])
def get_user_groups_endpoint(user_id: UUID, db: Session = Depends(get_db)):
    groups = get_user_groups(db=db, user_id=user_id)
    return groups


@router.get("/{group_id}/ranking", response_model=list[GroupUserPositions])
def get_group_members_endpoint(group_id: UUID, db: Session = Depends(get_db)):
    members = get_group_members(db=db, group_id=group_id)
    return [
        GroupUserPositions(
            user_id=member.user_id,
            group_id=member.group_id,
            username=member.user.username,
            email=member.user.email,
            first_name=member.user.first_name,
            last_name=member.user.last_name,
            user_score=prediction.user_score,
        )
        for member, prediction in members
    ]
