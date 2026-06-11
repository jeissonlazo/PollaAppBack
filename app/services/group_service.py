from datetime import datetime
from uuid import UUID
import random
import string

from sqlalchemy import DateTime
from sqlalchemy.orm import Session

from app.models.group import Group, GroupMember

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
    tournament_id: int,
    users_limit: int,
    description: str = None,
    observations: str = None,
):
    group = Group(
        admin_id=admin_id,
        name=name,
        users_limit=users_limit,
        description=description,
        observations=observations,
        tournament_id=tournament_id,
        invite_code=generate_invite_code(),
    )

    db.add(group)
    db.commit()
    db.refresh(group)
    add_user_to_group(db=db, group_id=group.group_id, user_id=admin_id)
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


def get_user_groups(db: Session, user_id: UUID):

    return (
        db.query(Group)
        .join(GroupMember, Group.group_id == GroupMember.group_id)
        .filter(GroupMember.user_id == user_id)
        .all()
    )


def update_group(
    db: Session,
    group_id: UUID,
    name: str,
    users_limit: int,
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


def add_user_to_group_by_invite_code(db: Session, invite_code: str, user_id: UUID):
    # Buscar grupo
    group = db.query(Group).filter(Group.invite_code == invite_code).first()

    if not group:
        return None

    # Verificar si ya pertenece al grupo
    existing_member = (
        db.query(GroupMember)
        .filter(GroupMember.group_id == group.group_id, GroupMember.user_id == user_id)
        .first()
    )

    if existing_member:
        return existing_member

    # Verificar límite de usuarios
    members_count = (
        db.query(GroupMember).filter(GroupMember.group_id == group.group_id).count()
    )

    if members_count >= group.users_limit:
        raise Exception("Group is full")

    # Agregar usuario
    group_member = GroupMember(
        group_id=group.group_id, user_id=user_id, joined_at=datetime.utcnow()
    )

    db.add(group_member)
    db.commit()
    db.refresh(group_member)

    return group_member


def add_user_to_group(db: Session, group_id: UUID, user_id: UUID):
    group_member = GroupMember(
        group_id=group_id, user_id=user_id, joined_at=datetime.utcnow()
    )

    db.add(group_member)
    db.commit()
    db.refresh(group_member)

    return group_member
