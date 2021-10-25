from typing import List

from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from pdip.dependency.container import DependencyContainer
from scheduler.domain.dao.connection.Connection import Connection
from scheduler.domain.dao.connection.ConnectorType import ConnectorType
from scheduler.domain.dao.Entity import Entity


class ConnectionType(Entity, DependencyContainer.Base):
    __tablename__ = "ConnectionType"
    __table_args__ = {"schema": "Connection"}
    Name = Column(String(100), index=False, unique=True, nullable=False)
    Connectors: List[ConnectorType] = relationship("ConnectorType",
                                                                  back_populates="ConnectionType")
    Connections: List[Connection] = relationship("Connection",
                                                                  back_populates="ConnectionType")

    def __init__(self,
                 Name: int = None,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.Name: int = Name
