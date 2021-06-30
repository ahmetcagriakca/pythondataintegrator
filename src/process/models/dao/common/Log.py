from sqlalchemy import Column, String, Integer, DateTime
from IocManager import IocManager
from models.base.common.LogBase import LogBase
from models.dao.Entity import Entity


class Log(LogBase,Entity, IocManager.Base):
    __tablename__ = "Log"
    __table_args__ = {"schema": "Common"}
    TypeId = Column(Integer, index=True, unique=False, nullable=False)
    Content = Column(String(4000), index=False, unique=False, nullable=True)
    LogDatetime = Column(DateTime, index=False, unique=False, nullable=True)
    JobId = Column(Integer, index=True, unique=False, nullable=True)