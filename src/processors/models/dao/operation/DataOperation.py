from models.dao.operation.DataOperationContact import DataOperationContact
from models.dao.operation.DataOperationJob import DataOperationJob
from typing import List
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from infrastructor.IocManager import IocManager
from models.dao.Entity import Entity
from models.dao.operation.DataOperationIntegration import DataOperationIntegration


class DataOperation(Entity, IocManager.Base):
    __tablename__ = "DataOperation"
    __table_args__ = {"schema": "Operation"}
    DefinitionId = Column(Integer, ForeignKey('Operation.Definition.Id'))
    Name = Column(String(100), index=True, unique=False, nullable=False)
    Definition = relationship("Definition", back_populates="DataOperations")
    DataOperationJobs: List[DataOperationJob] = relationship("DataOperationJob", back_populates="DataOperation")
    Integrations: List[DataOperationIntegration] = relationship("DataOperationIntegration",
                                                                back_populates="DataOperation")
    Contacts: List[DataOperationContact] = relationship("DataOperationContact",
                                                        back_populates="DataOperation")

    def __init__(self,
                 DefinitionId: int = None,
                 Name: str = None,
                 Definition=None,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.DefinitionId: int = DefinitionId
        self.Name: str = Name
        self.Definition = Definition
