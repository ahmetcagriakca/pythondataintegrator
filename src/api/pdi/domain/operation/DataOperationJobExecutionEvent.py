from datetime import datetime

from pdip.data.domain import Entity
from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from pdi.domain.base import Base
from pdi.domain.base.operation.DataOperationJobExecutionEventBase import DataOperationJobExecutionEventBase


class DataOperationJobExecutionEvent(DataOperationJobExecutionEventBase, Entity, Base):
    __tablename__ = "DataOperationJobExecutionEvent"
    __table_args__ = {"schema": "Operation"}
    DataOperationJobExecutionId = Column(Integer, ForeignKey('Operation.DataOperationJobExecution.Id'))
    EventId = Column(Integer, ForeignKey('Common.OperationEvent.Id'))
    EventDate = Column(DateTime, index=False, unique=False, nullable=False, default=datetime.now)
    Event = relationship("OperationEvent", back_populates="DataOperationJobExecutionEvents")
    DataOperationJobExecution = relationship("DataOperationJobExecution",
                                             back_populates="DataOperationJobExecutionEvents")
