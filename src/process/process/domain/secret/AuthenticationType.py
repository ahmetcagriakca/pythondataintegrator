
from typing import List

from process.domain.base.secret.AuthenticationTypeBase import AuthenticationTypeBase
from process.domain.secret.SecretSource import SecretSource
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from process.domain.base import Base
from pdip.data import Entity


class AuthenticationType(AuthenticationTypeBase, Entity, Base):
    __tablename__ = "AuthenticationType"
    __table_args__ = {"schema": "Secret"}
    SecretTypeId = Column(Integer, ForeignKey('Secret.SecretType.Id'))
    Name = Column(String(100), index=False, unique=True, nullable=False)
    SecretType = relationship("SecretType", back_populates="AuthenticationTypes")
    SecretSources: List[SecretSource] = relationship("SecretSource", back_populates="AuthenticationType")

    def __init__(*args,**kwargs):
        super().__init__(*args,**kwargs)