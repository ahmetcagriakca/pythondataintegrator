from models.dao.Entity import Entity
from sqlalchemy import Column, String, Boolean, Float, TEXT, REAL, Integer, LargeBinary, Unicode, ForeignKey
from sqlalchemy.orm import relationship
from infrastructor.IocManager import IocManager


class ApSchedulerJobEvent(Entity, IocManager.Base):
    # TODO: This feels bad man
    __tablename__ = "ApSchedulerJobEvent"
    __table_args__ = {"schema": "Aps"}
    ApSchedulerJobId = Column(Integer, ForeignKey('Aps.ApSchedulerJob.Id'))
    EventId = Column(Integer, ForeignKey('Aps.ApSchedulerEvent.Id'))
    ApSchedulerJob = relationship("ApSchedulerJob", back_populates="JobEvents")
    def __init__(self,
                 EventId: int = None,
                 ApSchedulerJobId: str = None,
                 ApSchedulerJob=None,
                 ApSchedulerEvent=None,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.EventId: int = EventId
        self.ApSchedulerJobId: str = ApSchedulerJobId
        self.ApSchedulerJob = ApSchedulerJob
        self.ApSchedulerEvent = ApSchedulerEvent
