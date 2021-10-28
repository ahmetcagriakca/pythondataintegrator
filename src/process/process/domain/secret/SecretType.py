from typing import List

from pdip.data import Entity
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from process.domain.base import Base
from process.domain.base.secret.SecretTypeBase import SecretTypeBase
from process.domain.secret.AuthenticationType import AuthenticationType
from process.domain.secret.Secret import Secret


class SecretType(SecretTypeBase, Entity, Base):
    __tablename__ = "SecretType"
    __table_args__ = {"schema": "Secret"}
    Name = Column(String(100), index=False, unique=True, nullable=False)
    Secrets: List[Secret] = relationship("Secret", back_populates="SecretType")
    AuthenticationTypes: List[AuthenticationType] = relationship("AuthenticationType", back_populates="SecretType")

    def __init__(*args, **kwargs):
        super().__init__(*args, **kwargs)
