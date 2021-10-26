from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from scheduler.domain.base import Base
from typing import List

from pdip.data import Entity
from scheduler.domain.operation.DataOperationJobExecution import DataOperationJobExecution
from scheduler.domain.operation.DataOperationJobExecutionIntegration import DataOperationJobExecutionIntegration


class Status(Entity, Base):
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
