from typing import List

from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship

from pdip.dependency.container import DependencyContainer
from scheduler.domain.dao.Entity import Entity
from scheduler.domain.dao.connection.ConnectionSecret import ConnectionSecret
from scheduler.domain.dao.secret.SecretSource import SecretSource


class Secret(Entity, DependencyContainer.Base):
    __tablename__ = "Secret"
    __table_args__ = {"schema": "Secret"}
    SecretTypeId = Column(Integer, ForeignKey('Secret.SecretType.Id'))
    Name = Column(String(100), index=True, unique=False, nullable=False)
    SecretType = relationship("SecretType", back_populates="Secrets")
    SecretSources: List[SecretSource] = relationship("SecretSource", back_populates="Secret")
    ConnectionSecrets: List[ConnectionSecret] = relationship("ConnectionSecret", back_populates="Secret")

    def __init__(self,
                 SecretTypeId: int = None,
                 Name: str = None,
                 SecretType = None,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.SecretTypeId: int = SecretTypeId
        self.Name: str = Name
        self.SecretType = SecretType
