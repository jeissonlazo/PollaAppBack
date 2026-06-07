from sqlalchemy import Column, func
from sqlalchemy import String

from sqlalchemy import Integer
from app.core.database import Base


class Tournament(Base):
    __tablename__ = "tournament"

    id = Column(Integer, primary_key=True, autoincrement=True)

    name = Column(String(100), nullable=False)
