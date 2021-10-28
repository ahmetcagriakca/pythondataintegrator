from typing import List

from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from models.dao.base import Base
from models.base.operation.DataOperationIntegrationBase import DataOperationIntegrationBase
from pdip.data import Entity
from models.dao.operation.DataOperationJobExecutionIntegration import DataOperationJobExecutionIntegration


class DataOperationIntegration(DataOperationIntegrationBase, Entity, Base):
    __tablename__ = "DataOperationIntegration"
    __table_args__ = {"schema": "Operation"}
    DataOperationId = Column(Integer, ForeignKey('Operation.DataOperation.Id'))
    DataIntegrationId = Column(Integer, ForeignKey('Integration.DataIntegration.Id'))
    Order = Column(Integer, index=False, unique=False, nullable=False)
    Limit = Column(Integer, index=False, unique=False, nullable=False)
    ProcessCount = Column(Integer, index=False, unique=False, nullable=False)
    DataOperation = relationship("DataOperation", back_populates="Integrations")
    DataIntegration = relationship("DataIntegration", back_populates="DataOperationIntegrations")
    DataOperationJobExecutionIntegrations: List[DataOperationJobExecutionIntegration] = relationship(
        "DataOperationJobExecutionIntegration",
        back_populates="DataOperationIntegration")

