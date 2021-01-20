from datetime import datetime
from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from infrastructor.IocManager import IocManager
from models.dao.Entity import Entity


class DataOperationJobExecution(Entity, IocManager.Base):
    __tablename__ = "DataOperationJobExecution"
    __table_args__ = {"schema": "Operation"}
    DataOperationJobId = Column(Integer, ForeignKey('Operation.DataOperationJob.Id'))
    DefinitionId = Column(Integer, ForeignKey('Operation.Definition.Id'))
    StatusId = Column(Integer, ForeignKey('Common.Status.Id'))
    StartDate = Column(DateTime, index=False, unique=False, nullable=False, default=datetime.now)
    EndDate = Column(DateTime, index=False, unique=False, nullable=True)
    Status = relationship("Status", back_populates="DataOperationJobExecutions")
    DataOperationJob = relationship("DataOperationJob", back_populates="DataOperationJobExecutions")
    DataOperationJobExecutionEvents = relationship("DataOperationJobExecutionEvent", back_populates="DataOperationJobExecution")
    DataOperationJobExecutionIntegrations = relationship("DataOperationJobExecutionIntegration", back_populates="DataOperationJobExecution")

    def __init__(self,
                 DataOperationId: int = None,
                 DataOperationJobId: int = None,
                 StatusId: int = None,
                 StartDate: datetime = None,
                 EndDate: datetime = None,
                 DataOperationJob=None,
                 Status=None,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.DataOperationId: int = DataOperationId
        self.DataOperationJobId: int = DataOperationJobId
        self.StatusId: int = StatusId
        self.StartDate: datetime = StartDate
        self.EndDate: datetime = EndDate
        self.DataOperationJob = DataOperationJob
        self.Status = Status
