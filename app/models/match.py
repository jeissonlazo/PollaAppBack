from uuid import uuid4

from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import Integer
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey

from sqlalchemy.dialects.postgresql import UUID

from app.core.database import Base


class Match(Base):
    __tablename__ = "matches"

    match_id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid4
    )

    round = Column(
        String(50),
        nullable=False
    )

    match_date = Column(
        DateTime,
        nullable=False
    )

    group_name = Column(
        String(10)
    )

    ground = Column(
        String(100)
    )

    team1_id = Column(
        UUID(as_uuid=True),
        ForeignKey("teams.team_id")
    )

    team2_id = Column(
        UUID(as_uuid=True),
        ForeignKey("teams.team_id")
    )

    score_team1 = Column(
        Integer,
        default=0
    )

    score_team2 = Column(
        Integer,
        default=0
    )