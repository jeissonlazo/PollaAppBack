from uuid import UUID

from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import status

from sqlalchemy.orm import Session

from app.core.database import get_db

from app.schemas.group import (
    GroupCreate,
    GroupResponse
)

from app.services.group_service import (
    create_group,
    get_group_by_id,
    update_group,
    delete_group
)

router = APIRouter(
    prefix="/groups",
    tags=["Groups"]
)


@router.post(
    "",
    response_model=GroupResponse,
    status_code=status.HTTP_201_CREATED
)
def create_group_endpoint(
    group: GroupCreate,
    db: Session = Depends(get_db)
):
    """
    Temporalmente el admin_id se recibe fijo.
    Luego se obtendrá desde el JWT.
    """

    admin_id = UUID(
        "11111111-1111-1111-1111-111111111111"
    )

    return create_group(
        db=db,
        admin_id=admin_id,
        name=group.name,
        users_limit=group.users_limit
    )


@router.get(
    "/{group_id}",
    response_model=GroupResponse
)
def get_group_endpoint(
    group_id: UUID,
    db: Session = Depends(get_db)
):
    group = get_group_by_id(
        db=db,
        group_id=group_id
    )

    if not group:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Group not found"
        )

    return group


@router.put(
    "/{group_id}",
    response_model=GroupResponse
)
def update_group_endpoint(
    group_id: UUID,
    group: GroupCreate,
    db: Session = Depends(get_db)
):
    updated_group = update_group(
        db=db,
        group_id=group_id,
        name=group.name,
        users_limit=group.users_limit
    )

    if not updated_group:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Group not found"
        )

    return updated_group


@router.delete(
    "/{group_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_group_endpoint(
    group_id: UUID,
    db: Session = Depends(get_db)
):
    deleted = delete_group(
        db=db,
        group_id=group_id
    )

    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Group not found"
        )

    return None