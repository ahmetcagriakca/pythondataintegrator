from pdip.configuration.services import ConfigParameterBase
from pdip.data import Entity
from sqlalchemy import Column, String

from scheduler.domain.base import Base


class ConfigParameter(ConfigParameterBase, Entity, Base):
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
