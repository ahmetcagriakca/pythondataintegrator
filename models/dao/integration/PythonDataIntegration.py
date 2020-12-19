from typing import List

from sqlalchemy import Column, String, Boolean
from sqlalchemy.orm import relationship

from infrastructor.IocManager import IocManager
from models.dao.Entity import Entity
from models.dao.integration.PythonDataIntegrationColumn import PythonDataIntegrationColumn
from models.dao.integration.PythonDataIntegrationConnection import PythonDataIntegrationConnection
from models.dao.integration.PythonDataIntegrationJob import PythonDataIntegrationJob
from models.dao.integration.PyhtonDataIntegrationExecutionJob import PythonDataIntegrationExecutionJob
from models.dao.operation.DataOperationIntegration import DataOperationIntegration


class PythonDataIntegration(Entity, IocManager.Base):
    __tablename__ = "PythonDataIntegration"
    __table_args__ = {"schema": "Integration"}
    Code = Column(String(100), index=True, unique=True, nullable=False)
    IsTargetTruncate = Column(Boolean, index=False, unique=False, nullable=True)
    IsDelta = Column(Boolean, index=False, unique=False, nullable=True)
    Columns: List[PythonDataIntegrationColumn] = relationship("PythonDataIntegrationColumn",
                                                              back_populates="PythonDataIntegration")
    Connections: List[PythonDataIntegrationConnection] = relationship("PythonDataIntegrationConnection",
                                                                      back_populates="PythonDataIntegration")
    Jobs: List[PythonDataIntegrationJob] = relationship("PythonDataIntegrationJob",
                                                        back_populates="PythonDataIntegration")
    ExecutionJobs: List[PythonDataIntegrationExecutionJob] = relationship("PythonDataIntegrationExecutionJob",
                                                                        back_populates="PythonDataIntegration")
    
    DataOperationIntegrations: List[DataOperationIntegration] = relationship("DataOperationIntegration",
                                                                        back_populates="PythonDataIntegration")
    def __init__(self,
                 Code: str = None,
                 IsTargetTruncate: bool = None,
                 IsDelta: bool = None,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.Code: str = Code
        self.IsTargetTruncate: bool = IsTargetTruncate
        self.IsDelta = IsDelta
