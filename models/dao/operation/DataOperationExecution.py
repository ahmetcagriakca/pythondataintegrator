from datetime import datetime
from typing import List

from sqlalchemy import Column, String, Boolean, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from infrastructor.IocManager import IocManager
from models.dao.Entity import Entity
from models.dao.operation.DataOperationExecutionProcess import DataOperationExecutionProcess


class DataOperationExecution(Entity, IocManager.Base):
    __tablename__ = "DataOperationExecution"
    __table_args__ = {"schema": "Operation"}
    DataOperationId = Column(Integer, ForeignKey('Operation.DataOperation.Id'))
    ApSchedulerJobId = Column(Integer, ForeignKey('Aps.ApSchedulerJob.Id'))
    StatusId = Column(Integer, ForeignKey('Operation.DataOperationExecutionStatus.Id'))
    StartDate = Column(DateTime, index=False, unique=False, nullable=False, default=datetime.now)
    EndDate = Column(DateTime, index=False, unique=False, nullable=True)
    Status = relationship("DataOperationExecutionStatus", back_populates="DataOperationExecutions")
    DataOperation = relationship("DataOperation", back_populates="Executions")
    Processes: List[DataOperationExecutionProcess] = relationship("DataOperationExecutionProcess",
                                                                back_populates="DataOperationExecution")

    def __init__(self,
                 DataOperationId: int = None,
                 ApSchedulerJobId: int = None,
                 StatusId: int = None,
                 Status=None,
                 DataOperation=None,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.DataOperationId: int = DataOperationId
        self.ApSchedulerJobId: int = ApSchedulerJobId
        self.StatusId: int = StatusId
        self.Status = Status
        self.DataOperation = DataOperation
