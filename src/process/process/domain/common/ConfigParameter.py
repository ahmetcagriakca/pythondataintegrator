from pdip.configuration.services import ConfigParameterBase
from pdip.data import Entity
from sqlalchemy import Column, String

from process.domain.base import Base


class ConfigParameter(ConfigParameterBase, Entity, Base):
    __tablename__ = "ConfigParameter"
    __table_args__ = {"schema": "Common"}

    Name = Column(String(255), nullable=False)
    Type = Column(String(255), nullable=True)
    Value = Column(String(255), nullable=False)
    Description = Column(String(1000), nullable=False)
