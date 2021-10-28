from typing import List

from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship

from models.base.connection.ConnectionBase import ConnectionBase
from pdip.data import Entity
from models.dao.base import Base
from models.dao.connection.ConnectionQueue import ConnectionQueue
from models.dao.connection.ConnectionDatabase import ConnectionDatabase
from models.dao.connection.ConnectionFile import ConnectionFile
from models.dao.connection.ConnectionSecret import ConnectionSecret
from models.dao.connection.ConnectionServer import ConnectionServer
from models.dao.integration.DataIntegrationConnection import DataIntegrationConnection


class Connection(ConnectionBase, Entity, Base):
    __tablename__ = "Connection"
    __table_args__ = {"schema": "Connection"}
    Name = Column(String(100), index=True, unique=False, nullable=False)
    ConnectionTypeId = Column(Integer, ForeignKey('Connection.ConnectionType.Id'))

    Database: ConnectionDatabase = relationship("ConnectionDatabase", uselist=False, backref="Connection")
    File: ConnectionFile = relationship("ConnectionFile", uselist=False, backref="Connection")
    Queue: ConnectionQueue = relationship("ConnectionQueue", uselist=False, backref="Connection")
    ConnectionType = relationship("ConnectionType", back_populates="Connections")
    ConnectionSecrets: List[ConnectionSecret] = relationship("ConnectionSecret", back_populates="Connection")
    ConnectionServers: List[ConnectionServer] = relationship("ConnectionServer", back_populates="Connection")
    DataIntegrationConnections: List[DataIntegrationConnection] = relationship("DataIntegrationConnection",
                                                                               back_populates="Connection")
