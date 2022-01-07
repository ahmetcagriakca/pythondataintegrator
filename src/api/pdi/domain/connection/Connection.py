from typing import List

from pdip.data.domain import Entity
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship

from pdi.domain.base import Base
from pdi.domain.base.connection.ConnectionBase import ConnectionBase
from pdi.domain.connection.ConnectionBigData import ConnectionBigData
from pdi.domain.connection.ConnectionDatabase import ConnectionDatabase
from pdi.domain.connection.ConnectionFile import ConnectionFile
from pdi.domain.connection.ConnectionQueue import ConnectionQueue
from pdi.domain.connection.ConnectionSecret import ConnectionSecret
from pdi.domain.connection.ConnectionServer import ConnectionServer
from pdi.domain.integration.DataIntegrationConnection import DataIntegrationConnection


class Connection(ConnectionBase, Entity, Base):
    __tablename__ = "Connection"
    __table_args__ = {"schema": "Connection"}
    Name = Column(String(100), index=True, unique=False, nullable=False)
    ConnectionTypeId = Column(Integer, ForeignKey('Connection.ConnectionType.Id'))

    Database: ConnectionDatabase = relationship("ConnectionDatabase", uselist=False, backref="Connection")
    BigData: ConnectionBigData = relationship("ConnectionBigData", uselist=False, backref="Connection")
    File: ConnectionFile = relationship("ConnectionFile", uselist=False, backref="Connection")
    Queue: ConnectionQueue = relationship("ConnectionQueue", uselist=False, backref="Connection")
    ConnectionType = relationship("ConnectionType", back_populates="Connections")
    ConnectionSecrets: List[ConnectionSecret] = relationship("ConnectionSecret", back_populates="Connection")
    ConnectionServers: List[ConnectionServer] = relationship("ConnectionServer", back_populates="Connection")
    DataIntegrationConnections: List[DataIntegrationConnection] = relationship("DataIntegrationConnection",
                                                                               back_populates="Connection")
