from sqlalchemy.orm import Session
from sqlalchemy.orm import joinedload
from app.models.match import Match

def create_match(
    db: Session,
    match_data
):
    match = Match(**match_data.dict())

    db.add(match)
    db.commit()
    db.refresh(match)

    return match

def get_match_by_id(
    db: Session,
    match_id
):
    return (
        db.query(Match)
        .filter(
            Match.match_id == match_id
        )
        .first()
    )


def get_matches(
    db: Session
):
    return (
        db.query(Match).options(joinedload(Match.team1), joinedload(Match.team2)).all()
    )

def update_match(
    db: Session,
    match_id,
    match_data
):
    match = get_match_by_id(
        db,
        match_id
    )

    if not match:
        return None

    for key, value in match_data.dict().items():
        setattr(
            match,
            key,
            value
        )

    db.commit()
    db.refresh(match)

    return match


def delete_match(
    db: Session,
    match_id
):
    match = get_match_by_id(
        db,
        match_id
    )

    if not match:
        return False

    db.delete(match)
    db.commit()

    return True

def get_matches_by_round(
    db: Session,
    round_name: str
):
    return (
        db.query(Match)
        .filter(
            Match.round == round_name
        )
        .all()
    )
