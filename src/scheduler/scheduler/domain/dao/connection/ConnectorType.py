from scheduler.domain.dao.connection.ConnectionQueue import ConnectionQueue
from typing import List

from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from pdip.dependency.container import DependencyContainer
from scheduler.domain.dao.connection.ConnectionDatabase import ConnectionDatabase
from scheduler.domain.dao.connection.ConnectionFile import ConnectionFile
from scheduler.domain.dao.Entity import Entity


class ConnectorType(Entity, DependencyContainer.Base):
    __tablename__ = "ConnectorType"
    __table_args__ = {"schema": "Connection"}
    ConnectionTypeId = Column(Integer, ForeignKey('Connection.ConnectionType.Id'))
    Name = Column(String(100), index=False, unique=True, nullable=False)
    ConnectionType = relationship("ConnectionType", back_populates="Connectors")
    Databases: List[ConnectionDatabase] = relationship("ConnectionDatabase", back_populates="ConnectorType")
    Files: List[ConnectionFile] = relationship("ConnectionFile", back_populates="ConnectorType")
    Queues: List[ConnectionQueue] = relationship("ConnectionQueue", back_populates="ConnectorType")

    def __init__(self,
                 Name: int = None,
                 ConnectionTypeId: int = None,
                 ConnectionType = None,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.Name: int = Name
        self.ConnectionTypeId: int = ConnectionTypeId
        self.ConnectionType = ConnectionType
