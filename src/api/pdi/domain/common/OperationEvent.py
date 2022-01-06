from pdip.data.domain import Entity
from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship

from pdi.domain.base import Base
from pdi.domain.base.common.OperationEventBase import OperationEventBase


class OperationEvent(OperationEventBase, Entity, Base):
    __tablename__ = "OperationEvent"
    __table_args__ = {"schema": "Common"}
    Code = Column(Integer, index=False, unique=True, nullable=False)
    Name = Column(String(100), index=False, unique=False, nullable=False)
    Description = Column(String(250), index=False, unique=False, nullable=False)
    Class = Column(String(255), nullable=False)

    DataOperationJobExecutionEvents = relationship("DataOperationJobExecutionEvent", back_populates="Event")
    DataOperationJobExecutionIntegrationEvents = relationship("DataOperationJobExecutionIntegrationEvent",
                                                              back_populates="Event")
