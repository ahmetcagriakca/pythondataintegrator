from datetime import datetime
from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from infrastructor.IocManager import IocManager
from models.dao.Entity import Entity


class DataOperationJobExecutionEvent(Entity, IocManager.Base):
    __tablename__ = "DataOperationJobExecutionEvent"
    __table_args__ = {"schema": "Operation"}
    DataOperationJobExecutionId = Column(Integer, ForeignKey('Operation.DataOperationJobExecution.Id'))
    EventId = Column(Integer, ForeignKey('Common.OperationEvent.Id'))
    EventDate = Column(DateTime, index=False, unique=False, nullable=False, default=datetime.now)
    Event = relationship("OperationEvent", back_populates="DataOperationJobExecutionEvents")
    DataOperationJobExecution = relationship("DataOperationJobExecution", back_populates="DataOperationJobExecutionEvents")

    def __init__(self,
                 DataOperationJobExecutionId: int = None,
                 EventId: int = None,
                 EventDate: datetime = None,
                 DataOperationJobExecution=None,
                 Event=None,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.DataOperationJobExecutionId: int = DataOperationJobExecutionId
        self.EventId: int = EventId
        self.EventDate: int = EventDate
        self.DataOperationJobExecution = DataOperationJobExecution
        self.Event = Event
