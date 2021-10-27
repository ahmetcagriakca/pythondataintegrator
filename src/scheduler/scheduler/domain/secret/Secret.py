from typing import List

from pdip.data import Entity
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship

from scheduler.domain.base import Base
from scheduler.domain.connection.ConnectionSecret import ConnectionSecret
from scheduler.domain.secret.SecretSource import SecretSource


class Secret(Entity, Base):
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
                 SecretType=None,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.SecretTypeId: int = SecretTypeId
        self.Name: str = Name
        self.SecretType = SecretType
