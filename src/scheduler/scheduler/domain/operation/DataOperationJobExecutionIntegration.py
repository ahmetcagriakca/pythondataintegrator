from datetime import datetime
from typing import List

from sqlalchemy import Column, Integer, ForeignKey, DateTime, String
from sqlalchemy.orm import relationship
from scheduler.domain.base import Base
from pdip.data import Entity
from scheduler.domain.operation.DataOperationJobExecutionIntegrationEvent import DataOperationJobExecutionIntegrationEvent


class DataOperationJobExecutionIntegration(Entity, Base):
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
                 DataOperationJobExecutionId: int = None,
                 DataOperationIntegrationId: int = None,
                 StatusId: int = None,
                 StartDate: datetime = None,
                 EndDate: datetime = None,
                 Limit: int = None,
                 ProcessCount: int = None,
                 SourceDataCount: int = None,
                 Log: str = None,
                 DataOperationIntegration: any = None,
                 DataOperationJobExecution: any = None,
                 Status: any = None,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.DataOperationJobExecutionId: int = DataOperationJobExecutionId
        self.DataOperationIntegrationId: int = DataOperationIntegrationId
        self.StatusId: int = StatusId
        self.StartDate: datetime = StartDate
        self.EndDate: datetime = EndDate
        self.Limit: int = Limit
        self.ProcessCount: int = ProcessCount
        self.SourceDataCount: int = SourceDataCount
        self.Log: str = Log
        self.DataOperationIntegration: any = DataOperationIntegration
        self.DataOperationJobExecution: any = DataOperationJobExecution
        self.Status: any = Status
