from datetime import datetime
from typing import List

from pdip.data.domain import Entity
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from process.domain.base import Base
from process.domain.base.operation.DataOperationJobBase import DataOperationJobBase
from process.domain.operation.DataOperationJobExecution import DataOperationJobExecution


class DataOperationJob(DataOperationJobBase, Entity, Base):
    __tablename__ = "DataOperationJob"
    __table_args__ = {"schema": "Operation"}
    DataOperationId = Column(Integer, ForeignKey('Operation.DataOperation.Id'))
    ApSchedulerJobId = Column(Integer, ForeignKey('Aps.ApSchedulerJob.Id'))
    StartDate = Column(DateTime, index=False, unique=False, nullable=False, default=datetime.now)
    EndDate = Column(DateTime, index=False, unique=False, nullable=True)
    Cron = Column(String(100), index=False, unique=False, nullable=True)
    DataOperation = relationship("DataOperation", back_populates="DataOperationJobs")
    ApSchedulerJob = relationship("ApSchedulerJob", back_populates="DataOperationJobs")
    DataOperationJobExecutions: List[DataOperationJobExecution] = relationship("DataOperationJobExecution",
                                                                               back_populates="DataOperationJob")
