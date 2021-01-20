from datetime import datetime
from typing import List

from sqlalchemy import Column, Integer, ForeignKey, DateTime, String
from sqlalchemy.orm import relationship
from infrastructor.IocManager import IocManager
from models.dao.Entity import Entity
from models.dao.operation.DataOperationJobExecutionIntegrationEvent import DataOperationJobExecutionIntegrationEvent


class DataOperationJobExecutionIntegration(Entity, IocManager.Base):
    __tablename__ = "DataOperationJobExecutionIntegration"
    __table_args__ = {"schema": "Operation"}
    DataOperationJobExecutionId = Column(Integer, ForeignKey('Operation.DataOperationJobExecution.Id'))
    DataOperationIntegrationId = Column(Integer, ForeignKey('Operation.DataOperationIntegration.Id'))
    StatusId = Column(Integer, ForeignKey('Common.Status.Id'))
    StartDate = Column(DateTime, index=False, unique=False, nullable=False, default=datetime.now)
    EndDate = Column(DateTime, index=False, unique=False, nullable=True)
    Limit = Column(Integer, index=False, unique=False, nullable=True)
    ProcessCount = Column(Integer, index=False, unique=False, nullable=True)
    SourceDataCount = Column(Integer, index=False, unique=False, nullable=True)
    Log = Column(String(1000), index=False, unique=False, nullable=True)
    Status = relationship("Status", back_populates="DataOperationJobExecutionIntegrations")
    DataOperationIntegration = relationship("DataOperationIntegration",
                                            back_populates="DataOperationJobExecutionIntegrations")
    DataOperationJobExecution = relationship("DataOperationJobExecution",
                                             back_populates="DataOperationJobExecutionIntegrations")
    DataOperationJobExecutionIntegrationEvents: List[DataOperationJobExecutionIntegrationEvent] = relationship(
        "DataOperationJobExecutionIntegrationEvent",
        back_populates="DataOperationJobExecutionIntegration")

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
