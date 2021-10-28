from models.base.connection.ConnectorTypeBase import ConnectorTypeBase
from models.dao.connection.ConnectionQueue import ConnectionQueue
from typing import List

from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from models.dao.base import Base
from models.dao.connection.ConnectionDatabase import ConnectionDatabase
from models.dao.connection.ConnectionFile import ConnectionFile
from pdip.data import Entity


class ConnectorType(ConnectorTypeBase, Entity, Base):
    __tablename__ = "ConnectorType"
    __table_args__ = {"schema": "Connection"}
    ConnectionTypeId = Column(Integer, ForeignKey('Connection.ConnectionType.Id'))
    Name = Column(String(100), index=False, unique=True, nullable=False)
    ConnectionType = relationship("ConnectionType", back_populates="Connectors")
    Databases: List[ConnectionDatabase] = relationship("ConnectionDatabase", back_populates="ConnectorType")
    Files: List[ConnectionFile] = relationship("ConnectionFile", back_populates="ConnectorType")
    Queues: List[ConnectionQueue] = relationship("ConnectionQueue", back_populates="ConnectorType")