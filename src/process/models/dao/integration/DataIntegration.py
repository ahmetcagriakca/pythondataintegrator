from typing import List

from sqlalchemy import Column, String, Boolean, Integer, ForeignKey
from sqlalchemy.orm import relationship

from models.dao.base import Base
from models.base.integration.DataIntegrationBase import DataIntegrationBase
from pdip.data import Entity
from models.dao.integration.DataIntegrationColumn import DataIntegrationColumn
from models.dao.integration.DataIntegrationConnection import DataIntegrationConnection
from models.dao.operation.DataOperationIntegration import DataOperationIntegration


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
