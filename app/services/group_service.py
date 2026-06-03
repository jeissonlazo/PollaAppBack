from uuid import UUID
import random
import string

from sqlalchemy.orm import Session

from app.models.group import Group


def generate_invite_code(length: int = 8) -> str:
    return ''.join(
        random.choices(
            string.ascii_uppercase + string.digits,
            k=length
        )
    )


def create_group(
    db: Session,
    admin_id: UUID,
    name: str,
    users_limit: int
):
    group = Group(
        admin_id=admin_id,
        name=name,
        users_limit=users_limit,
        invite_code=generate_invite_code()
    )

    db.add(group)
    db.commit()
    db.refresh(group)

    return group


def get_group_by_id(
    db: Session,
    group_id: UUID
):
    return (
        db.query(Group)
        .filter(Group.group_id == group_id)
        .first()
    )


def update_group(
    db: Session,
    group_id: UUID,
    name: str,
    users_limit: int
):
    group = get_group_by_id(
        db=db,
        group_id=group_id
    )

    if not group:
        return None

    group.name = name
    group.users_limit = users_limit

    db.commit()
    db.refresh(group)

    return group


def delete_group(
    db: Session,
    group_id: UUID
):
    group = get_group_by_id(
        db=db,
        group_id=group_id
    )

    if not group:
        return False

    db.delete(group)
    db.commit()

    return True