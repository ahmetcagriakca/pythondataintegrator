from datetime import datetime
from typing import List

from pdip.data.domain import Entity
from sqlalchemy import Column, Integer, ForeignKey, DateTime, String
from sqlalchemy.orm import relationship

from process.domain.base import Base
from process.domain.base.operation.DataOperationJobExecutionIntegrationBase import \
    DataOperationJobExecutionIntegrationBase
from process.domain.operation.DataOperationJobExecutionIntegrationEvent import DataOperationJobExecutionIntegrationEvent


class DataOperationJobExecutionIntegration(DataOperationJobExecutionIntegrationBase, Entity, Base):
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
