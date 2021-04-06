from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from infrastructor.IocManager import IocManager
from models.dao.Entity import Entity


class ConnectionServer(Entity, IocManager.Base):
    __tablename__ = "ConnectionServer"
    __table_args__ = {"schema": "Connection"}
    ConnectionId = Column(Integer, ForeignKey('Connection.Connection.Id'))
    Host = Column(String(100), index=False, unique=False, nullable=True)
    Port = Column(Integer, index=False, unique=False, nullable=True)
    Connection = relationship("Connection", back_populates="ConnectionServers")

    def __init__(self,
                 ConnectionId: int = None,
                 Host: str = None,
                 Port: int = None,
                 Connection=None,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ConnectionId: str = ConnectionId
        self.Host: str = Host
        self.Port: int = Port
        self.Connection = Connection
