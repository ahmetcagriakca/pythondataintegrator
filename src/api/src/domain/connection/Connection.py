from typing import List

from pdip.data.domain import Entity
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship

from src.domain.base import Base
from src.domain.base.connection.ConnectionBase import ConnectionBase
from src.domain.connection import ConnectionWebService
from src.domain.connection.ConnectionBigData import ConnectionBigData
from src.domain.connection.ConnectionDatabase import ConnectionDatabase
from src.domain.connection.ConnectionFile import ConnectionFile
from src.domain.connection.ConnectionQueue import ConnectionQueue
from src.domain.connection.ConnectionSecret import ConnectionSecret
from src.domain.connection.ConnectionServer import ConnectionServer
from src.domain.integration.DataIntegrationConnection import DataIntegrationConnection


class Connection(ConnectionBase, Entity, Base):
    __tablename__ = "Connection"
    __table_args__ = {"schema": "Connection"}
    Name = Column(String(100), index=True, unique=False, nullable=False)
    ConnectionTypeId = Column(Integer, ForeignKey('Connection.ConnectionType.Id'))

    Database: ConnectionDatabase = relationship("ConnectionDatabase", uselist=False, backref="Connection")
    BigData: ConnectionBigData = relationship("ConnectionBigData", uselist=False, backref="Connection")
    File: ConnectionFile = relationship("ConnectionFile", uselist=False, backref="Connection")
    Queue: ConnectionQueue = relationship("ConnectionQueue", uselist=False, backref="Connection")
    WebService: ConnectionWebService = relationship("ConnectionWebService", uselist=False, backref="Connection")
    ConnectionType = relationship("ConnectionType", back_populates="Connections")
    ConnectionSecrets: List[ConnectionSecret] = relationship("ConnectionSecret", back_populates="Connection")
    ConnectionServers: List[ConnectionServer] = relationship("ConnectionServer", back_populates="Connection")
    DataIntegrationConnections: List[DataIntegrationConnection] = relationship("DataIntegrationConnection",
                                                                               back_populates="Connection")
