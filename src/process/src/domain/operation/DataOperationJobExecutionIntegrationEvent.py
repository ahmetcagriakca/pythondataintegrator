from datetime import datetime

from pdip.data.domain import Entity
from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from src.domain.base import Base
from src.domain.base.operation.DataOperationJobExecutionIntegrationEventBase import \
    DataOperationJobExecutionIntegrationEventBase


class DataOperationJobExecutionIntegrationEvent(DataOperationJobExecutionIntegrationEventBase, Entity, Base):
    __tablename__ = "DataOperationJobExecutionIntegrationEvent"
    __table_args__ = {"schema": "Operation"}
    DataOperationJobExecutionIntegrationId = Column(Integer,
                                                    ForeignKey('Operation.DataOperationJobExecutionIntegration.Id'))
    EventId = Column(Integer, ForeignKey('Common.OperationEvent.Id'))
    EventDate = Column(DateTime, index=False, unique=False, nullable=False, default=datetime.now)
    AffectedRowCount = Column(Integer, index=False, unique=False, nullable=True)
    Event = relationship("OperationEvent", back_populates="DataOperationJobExecutionIntegrationEvents")
    DataOperationJobExecutionIntegration = relationship("DataOperationJobExecutionIntegration",
                                                        back_populates="DataOperationJobExecutionIntegrationEvents")
