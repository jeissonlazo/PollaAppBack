# app/models/team.py

from uuid import uuid4

from sqlalchemy import Column
from sqlalchemy import String, Integer

from sqlalchemy.dialects.postgresql import UUID

from app.core.database import Base


class Team(Base):
    __tablename__ = "teams"

    team_id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid4
    )

    country = Column(
        String(100),
        nullable=False
    )

    code = Column(
        String(3),
        unique=True,
        nullable=False
    )

    flag = Column(
        String(255),
        nullable=False
    )

    external_id = Column(Integer(), unique=True, nullable=True)
