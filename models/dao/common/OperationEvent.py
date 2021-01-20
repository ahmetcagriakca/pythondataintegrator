from typing import List

from sqlalchemy import Column, String, Boolean, Integer, ForeignKey
from sqlalchemy.orm import relationship

from infrastructor.IocManager import IocManager
from models.dao.Entity import Entity
from models.dao.operation.DataOperationJobExecution import DataOperationJobExecution


class OperationEvent(Entity,IocManager.Base):
    __tablename__ = "OperationEvent"
    __table_args__ = {"schema": "Common"}
    Code = Column(Integer, index=False, unique=True, nullable=False)
    Name = Column(String(100), index=False, unique=False, nullable=False)
    Description = Column(String(250), index=False, unique=False, nullable=False)
    Class = Column(String(255), nullable=False)
    
    DataOperationJobExecutionEvents = relationship("DataOperationJobExecutionEvent", back_populates="Event")
    DataOperationJobExecutionIntegrationEvents = relationship("DataOperationJobExecutionIntegrationEvent", back_populates="Event")

    def __init__(self,
                 Code: int = None,
                 Name: str = None,
                 Description: str = None,
                 Class: str = None,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.Code: int = Code
        self.Name: str = Name
        self.Description: str = Description
        self.Class: str = Class
