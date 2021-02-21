from models.dao.connection.ConnectionSecret import ConnectionSecret
from models.dao.connection.ConnectionDatabase import ConnectionDatabase
from models.dao.connection.ConnectionFile import ConnectionFile
from typing import List
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from infrastructor.IocManager import IocManager
from models.dao.Entity import Entity
from models.dao.integration.DataIntegrationConnection import DataIntegrationConnection


class Connection(Entity, IocManager.Base):
    __tablename__ = "Connection"
    __table_args__ = {"schema": "Connection"}
    Name = Column(String(100), index=True, unique=False, nullable=False)
    ConnectionTypeId = Column(Integer, ForeignKey('Connection.ConnectionType.Id'))

    Database: ConnectionDatabase = relationship("ConnectionDatabase", uselist=False, backref="Connection")
    File: ConnectionFile = relationship("ConnectionFile", uselist=False, backref="Connection")
    ConnectionType = relationship("ConnectionType", back_populates="Connections")
    ConnectionSecrets: List[ConnectionSecret] = relationship("ConnectionSecret", back_populates="Connection")
    DataIntegrationConnections: List[DataIntegrationConnection] = relationship("DataIntegrationConnection",
                                                                               back_populates="Connection")

    def __init__(self,
                 Name: str = None,
                 ConnectionTypeId: int = None,
                 ConnectionType=None,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.Name: str = Name
        self.ConnectionTypeId: int = ConnectionTypeId
        self.ConnectionType = ConnectionType
