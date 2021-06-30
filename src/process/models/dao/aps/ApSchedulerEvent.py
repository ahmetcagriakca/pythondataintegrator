from typing import List

from models.base.aps.ApSchedulerEventBase import ApSchedulerEventBase
from models.dao.aps.ApSchedulerJobEvent import ApSchedulerJobEvent
from models.dao.Entity import Entity
from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship
from IocManager import IocManager


class ApSchedulerEvent(ApSchedulerEventBase,Entity, IocManager.Base):
    __tablename__ = "ApSchedulerEvent"
    __table_args__ = {"schema": "Aps"}

    Code = Column(Integer, nullable=False)
    Name = Column(String(255), nullable=False)
    Description = Column(String(1000), nullable=False)
    Class = Column(String(255), nullable=False)
    JobEvents: List[ApSchedulerJobEvent] = relationship("ApSchedulerJobEvent", back_populates="ApSchedulerEvent")
