from typing import List

from pdip.data.domain import Entity
from sqlalchemy import Column, String, Boolean, Integer, ForeignKey
from sqlalchemy.orm import relationship

from src.domain.base import Base
from src.domain.integration.DataIntegrationColumn import DataIntegrationColumn
from src.domain.integration.DataIntegrationConnection import DataIntegrationConnection
from src.domain.operation.DataOperationIntegration import DataOperationIntegration


class DataIntegration(Entity, Base):
    __tablename__ = "DataIntegration"
    __table_args__ = {"schema": "Integration"}
    DefinitionId = Column(Integer, ForeignKey('Operation.Definition.Id'))
    Code = Column(String(100), index=True, unique=False, nullable=False)
    IsTargetTruncate = Column(Boolean, index=False, unique=False, nullable=True)
    IsDelta = Column(Boolean, index=False, unique=False, nullable=True)
    Definition = relationship("Definition", back_populates="DataIntegrations")
    Columns: List[DataIntegrationColumn] = relationship("DataIntegrationColumn",
                                                        back_populates="DataIntegration")
    Connections: List[DataIntegrationConnection] = relationship("DataIntegrationConnection",
                                                                back_populates="DataIntegration")

    DataOperationIntegrations: List[DataOperationIntegration] = relationship("DataOperationIntegration",
                                                                             back_populates="DataIntegration")

    def __init__(self,
                 DefinitionId: int = None,
                 Code: str = None,
                 IsTargetTruncate: bool = None,
                 IsDelta: bool = None,
                 Definition=None,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.DefinitionId: int = DefinitionId
        self.Code: str = Code
        self.IsTargetTruncate: bool = IsTargetTruncate
        self.IsDelta = IsDelta
        self.Definition = Definition
