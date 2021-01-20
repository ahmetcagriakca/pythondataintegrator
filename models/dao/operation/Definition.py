from models.dao.operation.DataOperationContact import DataOperationContact
from models.dao.operation.DataOperationJob import DataOperationJob
from typing import List
from sqlalchemy import Column, String, Integer, Text
from sqlalchemy.orm import relationship
from infrastructor.IocManager import IocManager
from models.dao.Entity import Entity
from models.dao.operation.DataOperationIntegration import DataOperationIntegration


class Definition(Entity, IocManager.Base):
    __tablename__ = "Definition"
    __table_args__ = {"schema": "Operation"}
    Name = Column(String(100), index=False, unique=False, nullable=False)
    Version = Column(Integer, index=False, unique=False, nullable=False)
    Content = Column(Text, index=False, unique=False, nullable=True)
    IsActive = Column(Integer, index=False, unique=False, nullable=False)


    def __init__(self,
                 Name: str = None,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.Name: str = Name
