from typing import List

from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from pdip.dependency.container import DependencyContainer
from pdip.data import Entity
from models.dao.operation import DataOperationJobExecution
from models.dao.operation.DataOperationJobExecutionIntegration import DataOperationJobExecutionIntegration


class Status(Entity, DependencyContainer.Base):
    __tablename__ = "Status"
    __table_args__ = {"schema": "Common"}
    Name = Column(String(100), index=False, unique=False, nullable=False)
    Description = Column(String(250), index=False, unique=False, nullable=False)
    DataOperationJobExecutions: List[DataOperationJobExecution] = relationship("DataOperationJobExecution",
                                                                               back_populates="Status")
    DataOperationJobExecutionIntegrations: List[DataOperationJobExecutionIntegration] = relationship(
        "DataOperationJobExecutionIntegration",
        back_populates="Status")

    def __init__(self,
                 Id: int = None,
                 Name: str = None,
                 Description: bool = None,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.Id: str = Id
        self.Name: str = Name
        self.Description: bool = Description
