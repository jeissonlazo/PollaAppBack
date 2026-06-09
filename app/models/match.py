from uuid import uuid4

from sqlalchemy import Boolean, Column, func
from sqlalchemy import String
from sqlalchemy import Integer
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from app.models.team import Team
from app.core.database import Base


class Match(Base):
    __tablename__ = "matches"

    match_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)

    round = Column(String(50), nullable=False)

    time = Column(String(20))

    match_date = Column(DateTime, nullable=False)

    group_name = Column(String(10))

    ground = Column(String(100))

    team1_id = Column(UUID(as_uuid=True), ForeignKey("teams.team_id"))

    team2_id = Column(UUID(as_uuid=True), ForeignKey("teams.team_id"))

    team1 = relationship("Team", foreign_keys=[team1_id])

    team2 = relationship("Team", foreign_keys=[team2_id])

    score_team1 = Column(Integer, default=0)

    score_team2 = Column(Integer, default=0)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    finish = Column(Boolean, default=False)

    defined = Column(Boolean, default=False)
