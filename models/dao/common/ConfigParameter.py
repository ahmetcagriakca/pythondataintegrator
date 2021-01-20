from typing import List
from models.dao.aps.ApSchedulerJobEvent import ApSchedulerJobEvent
from models.dao.Entity import Entity
from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship
from infrastructor.IocManager import IocManager


class ConfigParameter(Entity, IocManager.Base):
    __tablename__ = "ConfigParameter"
    __table_args__ = {"schema": "Common"}

    Name = Column(String(255), nullable=False)
    Type = Column(String(255), nullable=True)
    Value = Column(String(255), nullable=False)
    Description = Column(String(1000), nullable=False)

    def __init__(self,
                 Name: str = None,
                 Type: str = None,
                 Value: str = None,
                 Description: str = None,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.Name: str = Name
        self.Type: str = Type
        self.Value: str = Value
        self.Description: str = Description
