from typing import List

from pdip.data.domain import Entity
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship

from src.domain.base import Base
from src.domain.base.secret.AuthenticationTypeBase import AuthenticationTypeBase
from src.domain.secret.SecretSource import SecretSource


class AuthenticationType(AuthenticationTypeBase, Entity, Base):
    __tablename__ = "AuthenticationType"
    __table_args__ = {"schema": "Secret"}
    SecretTypeId = Column(Integer, ForeignKey('Secret.SecretType.Id'))
    Name = Column(String(100), index=False, unique=True, nullable=False)
    SecretType = relationship("SecretType", back_populates="AuthenticationTypes")
    SecretSources: List[SecretSource] = relationship("SecretSource", back_populates="AuthenticationType")

    def __init__(*args, **kwargs):
        super().__init__(*args, **kwargs)
