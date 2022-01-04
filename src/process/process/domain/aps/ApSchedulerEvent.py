from typing import List

from pdip.data.domain import Entity
from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship

from process.domain.aps.ApSchedulerJobEvent import ApSchedulerJobEvent
from process.domain.base import Base
from process.domain.base.aps.ApSchedulerEventBase import ApSchedulerEventBase


class ApSchedulerEvent(ApSchedulerEventBase, Entity, Base):
    __tablename__ = "ApSchedulerEvent"
    __table_args__ = {"schema": "Aps"}

    Code = Column(Integer, nullable=False)
    Name = Column(String(255), nullable=False)
    Description = Column(String(1000), nullable=False)
    Class = Column(String(255), nullable=False)
    JobEvents: List[ApSchedulerJobEvent] = relationship("ApSchedulerJobEvent", back_populates="ApSchedulerEvent")
