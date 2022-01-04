from typing import List

from pdip.data.domain import Entity
from sqlalchemy import Column, String, Boolean, Integer, ForeignKey
from sqlalchemy.orm import relationship

from process.domain.base import Base
from process.domain.base.integration.DataIntegrationBase import DataIntegrationBase
from process.domain.integration.DataIntegrationColumn import DataIntegrationColumn
from process.domain.integration.DataIntegrationConnection import DataIntegrationConnection
from process.domain.operation.DataOperationIntegration import DataOperationIntegration


class DataIntegration(DataIntegrationBase, Entity, Base):
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
