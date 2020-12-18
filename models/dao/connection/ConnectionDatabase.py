from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from infrastructor.IocManager import IocManager
from models.dao.Entity import Entity


class ConnectionDatabase(Entity, IocManager.Base):
    __tablename__ = "ConnectionDatabase"
    __table_args__ = {"schema": "Connection"}
    ConnectionId = Column(Integer, ForeignKey('Connection.Connection.Id'))
    ConnectorTypeId = Column(Integer, ForeignKey('Connection.ConnectorType.Id'))
    Host = Column(String(100), index=False, unique=False, nullable=True)
    Port = Column(Integer, index=False, unique=False, nullable=True)
    Sid = Column(String(100), index=False, unique=False, nullable=True)
    DatabaseName = Column(String(100), index=False, unique=False, nullable=True)
    User = Column(String(100), index=False, unique=False, nullable=True)
    Password = Column(String(100), index=False, unique=False, nullable=True)
    ConnectorType = relationship("ConnectorType", back_populates="Databases")

    def __init__(self,
                 ConnectionId: int = None,
                 ConnectorTypeId: int = None,
                 Host: str = None,
                 Port: int = None,
                 Sid: str = None,
                 DatabaseName: str = None,
                 User: str = None,
                 Password: str = None,
                 Connection = None,
                 ConnectorType = None,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ConnectionId: str = ConnectionId
        self.ConnectorTypeId: str = ConnectorTypeId
        self.Host: str = Host
        self.Port: int = Port
        self.Sid: str = Sid
        self.DatabaseName: str = DatabaseName
        self.User: str = User
        self.Password: str = Password
        self.Connection = Connection
        self.ConnectorType = ConnectorType