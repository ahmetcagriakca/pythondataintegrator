from typing import List

from pdip.data import Entity
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from scheduler.domain.base import Base
from scheduler.domain.operation.DataOperationJobExecutionIntegration import DataOperationJobExecutionIntegration


class DataOperationIntegration(Entity, Base):
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

    def __init__(self,
                 DataOperationId: int = None,
                 DataIntegrationId: int = None,
                 Order: int = None,
                 Limit: int = None,
                 ProcessCount: int = None,
                 DataOperation=None,
                 DataIntegration=None,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.DataOperationId: int = DataOperationId
        self.DataIntegrationId: int = DataIntegrationId
        self.Order: int = Order
        self.Limit: int = Limit
        self.ProcessCount: int = ProcessCount
        self.DataOperation = DataOperation
        self.DataIntegration = DataIntegration
