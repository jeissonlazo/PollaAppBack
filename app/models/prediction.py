from uuid import uuid4

from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import Boolean
from sqlalchemy import ForeignKey

from sqlalchemy.dialects.postgresql import UUID

from app.core.database import Base


class Prediction(Base):
    __tablename__ = "predictions"

    prediction_id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid4
    )

    prediction_set_id = Column(
        UUID(as_uuid=True),
        ForeignKey(
            "user_predictions.prediction_set_id"
        ),
        nullable=False
    )

    match_id = Column(
        UUID(as_uuid=True),
        ForeignKey("matches.match_id"),
        nullable=False
    )

    team1_id = Column(
        UUID(as_uuid=True),
        ForeignKey("teams.team_id"),
        nullable=False
    )

    team2_id = Column(
        UUID(as_uuid=True),
        ForeignKey("teams.team_id"),
        nullable=False
    )

    score_team1 = Column(
        Integer,
        nullable=False
    )

    score_team2 = Column(
        Integer,
        nullable=False
    )

    ended = Column(
        Boolean,
        default=False
    )