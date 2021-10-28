from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from models.dao.base import Base
from models.base.connection.ConnectionFileBase import ConnectionFileBase
from pdip.data import Entity


class ConnectionFile(ConnectionFileBase, Entity, Base):
    __tablename__ = "ConnectionFile"
    __table_args__ = {"schema": "Connection"}
    ConnectionId = Column(Integer, ForeignKey('Connection.Connection.Id'))
    ConnectorTypeId = Column(Integer, ForeignKey('Connection.ConnectorType.Id'))
    ConnectorType = relationship("ConnectorType", back_populates="Files")