from uuid import UUID
from sqlalchemy.orm import Session

from app.models.team import Team


def create_team(
    db: Session,
    country: str,
    code: str,
    flag: str
):
    team = Team(
        country=country,
        code=code,
        flag=flag
    )

    db.add(team)
    db.commit()
    db.refresh(team)

    return team


def get_teams(db: Session):
    return db.query(Team).all()


def get_team_by_id(
    db: Session,
    team_id: UUID
):
    return (
        db.query(Team)
        .filter(Team.team_id == team_id)
        .first()
    )


def update_team(
    db: Session,
    team_id: UUID,
    data: dict
):
    team = get_team_by_id(db, team_id)

    if not team:
        return None

    for key, value in data.items():
        if value is not None:
            setattr(team, key, value)

    db.commit()
    db.refresh(team)

    return team


def delete_team(
    db: Session,
    team_id: UUID
):
    team = get_team_by_id(db, team_id)

    if not team:
        return None

    db.delete(team)
    db.commit()

    return team