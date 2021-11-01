from typing import List

from pdip.data import Entity
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship

from pdi.domain.base import Base
from pdi.domain.base.secret.SecretBase import SecretBase
from pdi.domain.connection.ConnectionSecret import ConnectionSecret
from pdi.domain.secret.SecretSource import SecretSource


class Secret(SecretBase, Entity, Base):
    __tablename__ = "Secret"
    __table_args__ = {"schema": "Secret"}
    SecretTypeId = Column(Integer, ForeignKey('Secret.SecretType.Id'))
    Name = Column(String(100), index=True, unique=False, nullable=False)
    SecretType = relationship("SecretType", back_populates="Secrets")
    SecretSources: List[SecretSource] = relationship("SecretSource", back_populates="Secret")
    ConnectionSecrets: List[ConnectionSecret] = relationship("ConnectionSecret", back_populates="Secret")
