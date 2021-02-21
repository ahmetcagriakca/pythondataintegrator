from sqlalchemy import Column, String, Integer, ForeignKey, Text
from sqlalchemy.orm import relationship
from infrastructor.IocManager import IocManager
from models.dao.Entity import Entity


class ConnectionSecret(Entity, IocManager.Base):
    __tablename__ = "ConnectionSecret"
    __table_args__ = {"schema": "Connection"}
    ConnectionId = Column(Integer, ForeignKey('Connection.Connection.Id'))
    SecretId = Column(Integer, ForeignKey('Secret.Secret.Id'))
    Connection = relationship("Connection", back_populates="ConnectionSecrets")
    Secret = relationship("Secret", back_populates="ConnectionSecrets")

    def __init__(self,
                 ConnectionId: int = None,
                 SecretId: int = None,
                 Connection=None,
                 Secret=None,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.ConnectionId: int = ConnectionId
        self.SecretId: int = SecretId
        self.Connection = Connection
        self.Secret = Secret
