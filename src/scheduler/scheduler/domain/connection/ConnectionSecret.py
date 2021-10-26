from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from scheduler.domain.base import Base
from pdip.data import Entity


class ConnectionSecret(Entity, Base):
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
