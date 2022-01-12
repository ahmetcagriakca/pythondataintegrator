from pdip.data.domain import Entity
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from src.domain.base import Base


class ApSchedulerJobEvent(Entity, Base):
    __tablename__ = "ApSchedulerJobEvent"
    __table_args__ = {"schema": "Aps"}
    ApSchedulerJobId = Column(Integer, ForeignKey('Aps.ApSchedulerJob.Id'))
    EventId = Column(Integer, ForeignKey('Aps.ApSchedulerEvent.Id'))
    ApSchedulerJob = relationship("ApSchedulerJob", back_populates="JobEvents")
    ApSchedulerEvent = relationship("ApSchedulerEvent", back_populates="JobEvents")

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
