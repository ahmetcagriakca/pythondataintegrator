from typing import List

from pdip.data import Entity
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from pdi.domain.base import Base
from pdi.domain.base.secret.SecretTypeBase import SecretTypeBase
from pdi.domain.secret.AuthenticationType import AuthenticationType
from pdi.domain.secret.Secret import Secret


class SecretType(SecretTypeBase, Entity, Base):
    __tablename__ = "SecretType"
    __table_args__ = {"schema": "Secret"}
    Name = Column(String(100), index=False, unique=True, nullable=False)
    Secrets: List[Secret] = relationship("Secret", back_populates="SecretType")
    AuthenticationTypes: List[AuthenticationType] = relationship("AuthenticationType", back_populates="SecretType")
