from datetime import datetime

from pdip.data import Entity
from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from scheduler.domain.base import Base


class DataOperationJobExecutionIntegrationEvent(Entity, Base):
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

    def __init__(self,
                 DataOperationJobExecutionIntegrationId: int = None,
                 EventId: int = None,
                 EventDate: datetime = None,
                 AffectedRowCount: int = None,
                 Event: any = None,
                 DataOperationJobExecutionIntegration: any = None,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.DataOperationJobExecutionIntegrationId: int = DataOperationJobExecutionIntegrationId
        self.EventId: int = EventId
        self.EventDate: datetime = EventDate
        self.AffectedRowCount: int = AffectedRowCount
        self.Event = Event
        self.DataOperationJobExecutionIntegration = DataOperationJobExecutionIntegration
