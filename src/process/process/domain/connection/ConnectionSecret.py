from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from process.domain.base import Base
from process.domain.base.connection.ConnectionSecretBase import ConnectionSecretBase
from pdip.data import Entity


class ConnectionSecret(ConnectionSecretBase, Entity, Base):
    __tablename__ = "ConnectionSecret"
    __table_args__ = {"schema": "Connection"}
    ConnectionId = Column(Integer, ForeignKey('Connection.Connection.Id'))
    SecretId = Column(Integer, ForeignKey('Secret.Secret.Id'))
    Connection = relationship("Connection", back_populates="ConnectionSecrets")
    Secret = relationship("Secret", back_populates="ConnectionSecrets")
