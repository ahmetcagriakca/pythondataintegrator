from pdip.data.domain import Entity
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from src.domain.base import Base
from src.domain.base.connection.ConnectionFileBase import ConnectionFileBase


class ConnectionFile(ConnectionFileBase, Entity, Base):
    __tablename__ = "ConnectionFile"
    __table_args__ = {"schema": "Connection"}
    ConnectionId = Column(Integer, ForeignKey('Connection.Connection.Id'))
    ConnectorTypeId = Column(Integer, ForeignKey('Connection.ConnectorType.Id'))
    ConnectorType = relationship("ConnectorType", back_populates="Files")
