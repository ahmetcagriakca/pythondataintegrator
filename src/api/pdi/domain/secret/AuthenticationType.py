from typing import List

from pdip.data.domain import Entity
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship

from pdi.domain.base import Base
from pdi.domain.base.secret.AuthenticationTypeBase import AuthenticationTypeBase
from pdi.domain.secret.SecretSource import SecretSource


class AuthenticationType(AuthenticationTypeBase, Entity, Base):
    __tablename__ = "AuthenticationType"
    __table_args__ = {"schema": "Secret"}
    SecretTypeId = Column(Integer, ForeignKey('Secret.SecretType.Id'))
    Name = Column(String(100), index=False, unique=True, nullable=False)
    SecretType = relationship("SecretType", back_populates="AuthenticationTypes")
    SecretSources: List[SecretSource] = relationship("SecretSource", back_populates="AuthenticationType")
