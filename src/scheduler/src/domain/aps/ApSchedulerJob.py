from typing import List

from pdip.data.domain import Entity
from sqlalchemy import Column, String, TEXT, Unicode, DateTime
from sqlalchemy.orm import relationship

from src.domain.aps.ApSchedulerJobEvent import ApSchedulerJobEvent
from src.domain.base import Base
from src.domain.operation.DataOperationJob import DataOperationJob


class ApSchedulerJob(Entity, Base):
    __tablename__ = "ApSchedulerJob"
    __table_args__ = {"schema": "Aps"}

    JobId = Column(Unicode(191, _warn_on_bytestring=False))
    NextRunTime = Column(DateTime)
    FuncRef = Column(String(500), nullable=False)
    JobEvents: List[ApSchedulerJobEvent] = relationship("ApSchedulerJobEvent", back_populates="ApSchedulerJob")
    DataOperationJobs: List[DataOperationJob] = relationship("DataOperationJob", back_populates="ApSchedulerJob")

    def __init__(self,
                 JobId: TEXT = None,
                 NextRunTime: float = None,
                 FuncRef=None,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.JobId: int = JobId
        self.NextRunTime: str = NextRunTime
        self.FuncRef = FuncRef
