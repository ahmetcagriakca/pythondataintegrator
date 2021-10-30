from typing import List

from pdip.data import Entity
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from process.domain.base import Base
from process.domain.base.common.StatusBase import StatusBase
from process.domain.operation import DataOperationJobExecution
from process.domain.operation.DataOperationJobExecutionIntegration import DataOperationJobExecutionIntegration


class Status(StatusBase, Entity, Base):
    __tablename__ = "Status"
    __table_args__ = {"schema": "Common"}
    Name = Column(String(100), index=False, unique=False, nullable=False)
    Description = Column(String(250), index=False, unique=False, nullable=False)
    DataOperationJobExecutions: List[DataOperationJobExecution] = relationship("DataOperationJobExecution",
                                                                               back_populates="Status")
    DataOperationJobExecutionIntegrations: List[DataOperationJobExecutionIntegration] = relationship(
        "DataOperationJobExecutionIntegration",
        back_populates="Status")
