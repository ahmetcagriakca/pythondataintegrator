from datetime import datetime
from typing import List

from sqlalchemy import Column, String, Boolean, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from infrastructor.IocManager import IocManager
from models.dao.Entity import Entity
from models.dao.operation.DataOperationJobExecutionEvent import DataOperationJobExecutionEvent


class DataOperationJobExecution(Entity, IocManager.Base):
    __tablename__ = "DataOperationJobExecution"
    __table_args__ = {"schema": "Operation"}
    DataOperationJobId = Column(Integer, ForeignKey('Operation.DataOperationJob.Id'))
    StatusId = Column(Integer, ForeignKey('Common.Status.Id'))
    StartDate = Column(DateTime, index=False, unique=False, nullable=False, default=datetime.now)
    EndDate = Column(DateTime, index=False, unique=False, nullable=True)
    Status = relationship("Status", back_populates="DataOperationJobExecutions")
    DataOperationJob = relationship("DataOperationJob", back_populates="DataOperationJobExecutions")
    DataOperationJobExecutionEvents = relationship("DataOperationJobExecutionEvent", back_populates="DataOperationJobExecution")

    # Processes: List[DataOperationExecutionProcess] = relationship("DataOperationExecutionProcess",
    #                                                             back_populates="DataOperationJobExecution")
    # DataOperationExecutionEvents: List[DataOperationJobExecutionEvent] = relationship("DataOperationJobExecutionEvent",
    #                                                             back_populates="DataOperationJobExecution")

    def __init__(self,
                 DataOperationId: int = None,
                 DataOperationJobId: int = None,
                 StatusId: int = None,
                 StartDate: datetime = None,
                 EndDate: datetime = None,
                 DataOperation=None,
                 DataOperationJob=None,
                 Status=None,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.DataOperationId: int = DataOperationId
        self.DataOperationJobId: int = DataOperationJobId
        self.StatusId: int = StatusId
        self.StartDate: datetime = StartDate
        self.EndDate: datetime = EndDate
        self.DataOperation = DataOperation
        self.DataOperationJob = DataOperationJob
        self.Status = Status
