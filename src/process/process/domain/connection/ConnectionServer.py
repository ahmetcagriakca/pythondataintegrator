from pdip.data.domain import Entity
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship

from process.domain.base import Base
from process.domain.base.connection.ConnectionServerBase import ConnectionServerBase


class ConnectionServer(ConnectionServerBase, Entity, Base):
    __tablename__ = "ConnectionServer"
    __table_args__ = {"schema": "Connection"}
    ConnectionId = Column(Integer, ForeignKey('Connection.Connection.Id'))
    Host = Column(String(100), index=False, unique=False, nullable=True)
    Port = Column(Integer, index=False, unique=False, nullable=True)
    Connection = relationship("Connection", back_populates="ConnectionServers")
