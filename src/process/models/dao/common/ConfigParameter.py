from models.base.common.ConfigParameterBase import ConfigParameterBase
from models.dao.Entity import Entity
from sqlalchemy import Column, String
from IocManager import IocManager


class ConfigParameter(ConfigParameterBase,Entity, IocManager.Base):
    __tablename__ = "ConfigParameter"
    __table_args__ = {"schema": "Common"}

    Name = Column(String(255), nullable=False)
    Type = Column(String(255), nullable=True)
    Value = Column(String(255), nullable=False)
    Description = Column(String(1000), nullable=False)