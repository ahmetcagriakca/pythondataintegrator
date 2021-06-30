from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship
from IocManager import IocManager
from models.base.connection.ConnectionSecretBase import ConnectionSecretBase
from models.dao.Entity import Entity


class ConnectionSecret(ConnectionSecretBase,Entity, IocManager.Base):
    __tablename__ = "ConnectionSecret"
    __table_args__ = {"schema": "Connection"}
    ConnectionId = Column(Integer, ForeignKey('Connection.Connection.Id'))
    SecretId = Column(Integer, ForeignKey('Secret.Secret.Id'))
    Connection = relationship("Connection", back_populates="ConnectionSecrets")
    Secret = relationship("Secret", back_populates="ConnectionSecrets")
