from datetime import datetime
from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from IocManager import IocManager
from models.base.operation.DataOperationJobExecutionIntegrationEventBase import DataOperationJobExecutionIntegrationEventBase
from models.dao.Entity import Entity


class DataOperationJobExecutionIntegrationEvent(DataOperationJobExecutionIntegrationEventBase,Entity, IocManager.Base):
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