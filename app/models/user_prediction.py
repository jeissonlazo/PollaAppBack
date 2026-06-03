from uuid import uuid4

from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import ForeignKey

from sqlalchemy.dialects.postgresql import UUID

from app.core.database import Base


class UserPrediction(Base):
    __tablename__ = "user_predictions"

    prediction_set_id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid4
    )

    user_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=False
    )

    group_id = Column(
        UUID(as_uuid=True),
        ForeignKey("groups.group_id"),
        nullable=False
    )

    user_score = Column(
        Integer,
        default=0
    )