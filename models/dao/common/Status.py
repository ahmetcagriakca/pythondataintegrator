from typing import List

from sqlalchemy import Column, String, Boolean, Integer, ForeignKey
from sqlalchemy.orm import relationship

from infrastructor.IocManager import IocManager
from models.dao.Entity import Entity
from models.dao.operation import DataOperationJobExecution


class Status(Entity, IocManager.Base):
    __tablename__ = "Status"
    __table_args__ = {"schema": "Common"}
    Name = Column(String(100), index=False, unique=False, nullable=False)
    Description = Column(String(250), index=False, unique=False, nullable=False)
    DataOperationJobExecutions: List[DataOperationJobExecution] = relationship("DataOperationJobExecution",
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
