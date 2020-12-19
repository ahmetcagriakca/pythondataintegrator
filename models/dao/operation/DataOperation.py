from models.dao.operation.DataOperationJob import DataOperationJob
from typing import List

from sqlalchemy import Column, String, Boolean, Integer, DateTime
from sqlalchemy.orm import relationship

from infrastructor.IocManager import IocManager
from models.dao.Entity import Entity
from models.dao.operation.DataOperationIntegration import DataOperationIntegration
from models.dao.operation.DataOperationExecution import DataOperationExecution


class DataOperation(Entity, IocManager.Base):
    __tablename__ = "DataOperation"
    __table_args__ = {"schema": "Operation"}
    Name = Column(String(100), index=False, unique=False, nullable=False)
    Limit = Column(Integer, index=False, unique=False, nullable=False)
    ProcessCount = Column(Integer, index=False, unique=False, nullable=False)
    Executions: List[DataOperationExecution] = relationship("DataOperationExecution", back_populates="DataOperation")
    Jobs: List[DataOperationJob] = relationship("DataOperationJob", back_populates="DataOperation")
    Integrations: List[DataOperationIntegration] = relationship("DataOperationIntegration",
                                                                             back_populates="DataOperation")

    def __init__(self,
                 Name: str = None,
                 Limit: int = None,
                 ProcessCount: int = None,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.Name: str = Name
        self.Limit: int = Limit
        self.ProcessCount: int = ProcessCount
