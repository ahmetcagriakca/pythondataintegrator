from typing import List

from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from IocManager import IocManager
from models.base.connection.ConnectionTypeBase import ConnectionTypeBase
from models.dao.connection.Connection import Connection
from models.dao.connection.ConnectorType import ConnectorType
from models.dao.Entity import Entity


class ConnectionType(ConnectionTypeBase,Entity, IocManager.Base):
    __tablename__ = "ConnectionType"
    __table_args__ = {"schema": "Connection"}
    Name = Column(String(100), index=False, unique=True, nullable=False)
    Connectors: List[ConnectorType] = relationship("ConnectorType",
                                                                  back_populates="ConnectionType")
    Connections: List[Connection] = relationship("Connection",
                                                                  back_populates="ConnectionType")