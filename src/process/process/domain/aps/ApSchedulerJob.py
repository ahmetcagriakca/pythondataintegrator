from typing import List

from pdip.data import Entity
from sqlalchemy import Column, String, Unicode, DateTime
from sqlalchemy.orm import relationship

from process.domain.aps.ApSchedulerJobEvent import ApSchedulerJobEvent
from process.domain.base import Base
from process.domain.base.aps.ApSchedulerJobBase import ApSchedulerJobBase
from process.domain.operation.DataOperationJob import DataOperationJob


class ApSchedulerJob(ApSchedulerJobBase, Entity, Base):
    __tablename__ = "ApSchedulerJob"
    __table_args__ = {"schema": "Aps"}

    JobId = Column(Unicode(191, _warn_on_bytestring=False))
    NextRunTime = Column(DateTime)
    FuncRef = Column(String(500), nullable=False)
    JobEvents: List[ApSchedulerJobEvent] = relationship("ApSchedulerJobEvent", back_populates="ApSchedulerJob")
    DataOperationJobs: List[DataOperationJob] = relationship("DataOperationJob", back_populates="ApSchedulerJob")
