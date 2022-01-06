from typing import List

from pdip.data.domain import Entity
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from process.domain.base import Base
from process.domain.base.connection.ConnectionTypeBase import ConnectionTypeBase
from process.domain.connection.Connection import Connection
from process.domain.connection.ConnectorType import ConnectorType


class ConnectionType(ConnectionTypeBase, Entity, Base):
    __tablename__ = "ConnectionType"
    __table_args__ = {"schema": "Connection"}
    Name = Column(String(100), index=False, unique=True, nullable=False)
    Connectors: List[ConnectorType] = relationship("ConnectorType",
                                                   back_populates="ConnectionType")
    Connections: List[Connection] = relationship("Connection",
                                                 back_populates="ConnectionType")
