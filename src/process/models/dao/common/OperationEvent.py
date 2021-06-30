from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship

from IocManager import IocManager
from models.base.common.OperationEventBase import OperationEventBase
from models.dao.Entity import Entity


class OperationEvent(OperationEventBase,Entity,IocManager.Base):
    __tablename__ = "OperationEvent"
    __table_args__ = {"schema": "Common"}
    Code = Column(Integer, index=False, unique=True, nullable=False)
    Name = Column(String(100), index=False, unique=False, nullable=False)
    Description = Column(String(250), index=False, unique=False, nullable=False)
    Class = Column(String(255), nullable=False)
    
    DataOperationJobExecutionEvents = relationship("DataOperationJobExecutionEvent", back_populates="Event")
    DataOperationJobExecutionIntegrationEvents = relationship("DataOperationJobExecutionIntegrationEvent", back_populates="Event")
