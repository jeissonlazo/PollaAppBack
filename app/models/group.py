from uuid import uuid4

from sqlalchemy import Column
from sqlalchemy import String
from sqlalchemy import Integer
from sqlalchemy import ForeignKey
from sqlalchemy import DateTime
from sqlalchemy.sql import func

from sqlalchemy.dialects.postgresql import UUID

from app.core.database import Base


class Group(Base):
    __tablename__ = "groups"

    group_id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid4
    )

    admin_id = Column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=False
    )

    name = Column(
        String(100),
        nullable=False
    )

    users_limit = Column(
        Integer,
        nullable=False,
        default=10
    )

    invite_code = Column(
        String(20),
        unique=True,
        nullable=False
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )