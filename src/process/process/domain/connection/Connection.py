from typing import List

from pdip.data import Entity
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship

from process.domain.base import Base
from process.domain.base.connection.ConnectionBase import ConnectionBase
from process.domain.connection.ConnectionDatabase import ConnectionDatabase
from process.domain.connection.ConnectionFile import ConnectionFile
from process.domain.connection.ConnectionQueue import ConnectionQueue
from process.domain.connection.ConnectionSecret import ConnectionSecret
from process.domain.connection.ConnectionServer import ConnectionServer
from process.domain.integration.DataIntegrationConnection import DataIntegrationConnection


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
