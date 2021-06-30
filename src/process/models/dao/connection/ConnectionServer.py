from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from IocManager import IocManager
from models.base.connection.ConnectionServerBase import ConnectionServerBase
from models.dao.Entity import Entity


class ConnectionServer(ConnectionServerBase,Entity, IocManager.Base):
    __tablename__ = "ConnectionServer"
    __table_args__ = {"schema": "Connection"}
    ConnectionId = Column(Integer, ForeignKey('Connection.Connection.Id'))
    Host = Column(String(100), index=False, unique=False, nullable=True)
    Port = Column(Integer, index=False, unique=False, nullable=True)
    Connection = relationship("Connection", back_populates="ConnectionServers")