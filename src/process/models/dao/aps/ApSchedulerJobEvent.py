from models.base.aps.ApSchedulerJobEventBase import ApSchedulerJobEventBase
from models.dao.Entity import Entity
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from IocManager import IocManager


class ApSchedulerJobEvent(ApSchedulerJobEventBase,Entity, IocManager.Base):
    __tablename__ = "ApSchedulerJobEvent"
    __table_args__ = {"schema": "Aps"}
    ApSchedulerJobId = Column(Integer, ForeignKey('Aps.ApSchedulerJob.Id'))
    EventId = Column(Integer, ForeignKey('Aps.ApSchedulerEvent.Id'))
    ApSchedulerJob = relationship("ApSchedulerJob", back_populates="JobEvents")
    ApSchedulerEvent = relationship("ApSchedulerEvent", back_populates="JobEvents")
