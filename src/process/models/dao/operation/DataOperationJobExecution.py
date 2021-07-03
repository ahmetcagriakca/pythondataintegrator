from datetime import datetime
from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from IocManager import IocManager
from models.base.operation.DataOperationJobExecutionBase import DataOperationJobExecutionBase
from models.dao.Entity import Entity


class DataOperationJobExecution(DataOperationJobExecutionBase,Entity, IocManager.Base):
    __tablename__ = "DataOperationJobExecution"
    __table_args__ = {"schema": "Operation"}
    DefinitionId = Column(Integer, ForeignKey('Operation.Definition.Id'))
    DataOperationJobId = Column(Integer, ForeignKey('Operation.DataOperationJob.Id'))
    StatusId = Column(Integer, ForeignKey('Common.Status.Id'))
    StartDate = Column(DateTime, index=False, unique=False, nullable=False, default=datetime.now)
    EndDate = Column(DateTime, index=False, unique=False, nullable=True)
    Definition = relationship("Definition", back_populates="DataOperationJobExecutions")
    Status = relationship("Status", back_populates="DataOperationJobExecutions")
    DataOperationJob = relationship("DataOperationJob", back_populates="DataOperationJobExecutions")
    DataOperationJobExecutionEvents = relationship("DataOperationJobExecutionEvent", back_populates="DataOperationJobExecution")
    DataOperationJobExecutionIntegrations = relationship("DataOperationJobExecutionIntegration", back_populates="DataOperationJobExecution")
