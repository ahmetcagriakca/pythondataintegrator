from typing import List

from pdip.data import Entity
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from scheduler.domain.base import Base
from scheduler.domain.connection.Connection import Connection
from scheduler.domain.connection.ConnectorType import ConnectorType


class ConnectionType(Entity, Base):
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
