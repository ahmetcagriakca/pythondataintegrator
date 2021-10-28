from typing import List

from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship

from models.dao.base import Base
from models.base.secret.SecretBase import SecretBase
from pdip.data import Entity
from models.dao.connection.ConnectionSecret import ConnectionSecret
from models.dao.secret.SecretSource import SecretSource


class Secret(SecretBase, Entity, Base):
    __tablename__ = "Secret"
    __table_args__ = {"schema": "Secret"}
    SecretTypeId = Column(Integer, ForeignKey('Secret.SecretType.Id'))
    Name = Column(String(100), index=True, unique=False, nullable=False)
    SecretType = relationship("SecretType", back_populates="Secrets")
    SecretSources: List[SecretSource] = relationship("SecretSource", back_populates="Secret")
    ConnectionSecrets: List[ConnectionSecret] = relationship("ConnectionSecret", back_populates="Secret")

    def __init__(*args,**kwargs):
        super().__init__(*args,**kwargs)