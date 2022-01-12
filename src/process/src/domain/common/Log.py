from pdip.data.domain import Entity
from pdip.logging.domain import LogData
from sqlalchemy import Column, String, Integer, DateTime

from src.domain.base import Base


class Log(LogData, Entity, Base):
    __tablename__ = "Log"
    __table_args__ = {"schema": "Common"}
    TypeId = Column(Integer, index=True, unique=False, nullable=False)
    Content = Column(String(4000), index=False, unique=False, nullable=True)
    LogDatetime = Column(DateTime, index=False, unique=False, nullable=True)
    JobId = Column(Integer, index=True, unique=False, nullable=True)
