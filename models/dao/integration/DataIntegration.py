from typing import List

from sqlalchemy import Column, String, Boolean, Integer, ForeignKey
from sqlalchemy.orm import relationship

from infrastructor.IocManager import IocManager
from models.dao.Entity import Entity
from models.dao.integration.DataIntegrationColumn import DataIntegrationColumn
from models.dao.integration.DataIntegrationConnection import DataIntegrationConnection
from models.dao.integration.DataIntegrationExecutionJob import DataIntegrationExecutionJob
from models.dao.operation.DataOperationIntegration import DataOperationIntegration


class DataIntegration(Entity, IocManager.Base):
    __tablename__ = "DataIntegration"
    __table_args__ = {"schema": "Integration"}
    DefinitionId = Column(Integer, ForeignKey('Operation.Definition.Id'))
    Code = Column(String(100), index=True, unique=True, nullable=False)
    IsTargetTruncate = Column(Boolean, index=False, unique=False, nullable=True)
    IsDelta = Column(Boolean, index=False, unique=False, nullable=True)
    Definition = relationship("Definition", back_populates="DataIntegrations")
    Columns: List[DataIntegrationColumn] = relationship("DataIntegrationColumn",
                                                              back_populates="DataIntegration")
    Connections: List[DataIntegrationConnection] = relationship("DataIntegrationConnection",
                                                                      back_populates="DataIntegration")
    ExecutionJobs: List[DataIntegrationExecutionJob] = relationship("DataIntegrationExecutionJob",
                                                                        back_populates="DataIntegration")
    
    DataOperationIntegrations: List[DataOperationIntegration] = relationship("DataOperationIntegration",
                                                                        back_populates="DataIntegration")
    def __init__(self,
                 DefinitionId:int = None,
                 Code: str = None,
                 IsTargetTruncate: bool = None,
                 IsDelta: bool = None,
                 Definition = None,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.DefinitionId: int = DefinitionId
        self.Code: str = Code
        self.IsTargetTruncate: bool = IsTargetTruncate
        self.IsDelta = IsDelta
        self.Definition = Definition
