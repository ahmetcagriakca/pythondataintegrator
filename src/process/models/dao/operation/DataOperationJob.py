from datetime import datetime
from typing import List
from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from models.dao.base import Base
from models.base.operation.DataOperationJobBase import DataOperationJobBase
from pdip.data import Entity
from models.dao.operation.DataOperationJobExecution import DataOperationJobExecution


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
