from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from infrastructor.IocManager import IocManager
from models.dao.Entity import Entity


class ConnectionFile(Entity, IocManager.Base):
    __tablename__ = "ConnectionFile"
    __table_args__ = {"schema": "Connection"}
    ConnectionId = Column(Integer, ForeignKey('Connection.Connection.Id'))
    ConnectorTypeId = Column(Integer, ForeignKey('Connection.ConnectorType.Id'))
    ConnectorType = relationship("ConnectorType", back_populates="Files")

    def __init__(self,
                 ConnectionId: int = None,
                 ConnectorTypeId: int = None,
                 Connection=None,
                 ConnectorType=None,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ConnectionId: str = ConnectionId
        self.ConnectorTypeId: str = ConnectorTypeId
        self.Connection = Connection
        self.ConnectorType = ConnectorType
