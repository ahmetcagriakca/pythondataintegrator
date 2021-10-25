from datetime import datetime
from typing import List
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from pdip.dependency.container import DependencyContainer
from pdip.data import Entity
from models.dao.operation.DataOperationJobExecution import DataOperationJobExecution


class DataOperationJob(Entity, DependencyContainer.Base):
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

    def __init__(self,
                 DataOperationId: int = None,
                 ApSchedulerJobId: int = None,
                 StartDate: datetime = None,
                 EndDate: datetime = None,
                 Cron: str = None,
                 DataOperation=None,
                 ApSchedulerJob=None,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.DataOperationId: int = DataOperationId
        self.ApSchedulerJobId: int = ApSchedulerJobId
        self.StartDate: datetime = StartDate
        self.EndDate: datetime = EndDate
        self.Cron: int = Cron
        self.DataOperation = DataOperation
        self.ApSchedulerJob = ApSchedulerJob
