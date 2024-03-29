from typing import List

from pdip.data.domain import Entity
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from src.domain.base import Base
from src.domain.base.secret.SecretSourceBase import SecretSourceBase
from src.domain.secret.SecretSourceBasicAuthentication import SecretSourceBasicAuthentication
from src.domain.secret.SecretSourceKerberosAuthentication import SecretSourceKerberosAuthentication


class SecretSource(SecretSourceBase, Entity, Base):
    __tablename__ = "SecretSource"
    __table_args__ = {"schema": "Secret"}
    SecretId = Column(Integer, ForeignKey('Secret.Secret.Id'))
    AuthenticationTypeId = Column(Integer, ForeignKey('Secret.AuthenticationType.Id'))
    Secret = relationship("Secret", back_populates="SecretSources")
    AuthenticationType = relationship("AuthenticationType", back_populates="SecretSources")
    SecretSourceBasicAuthentications: List[SecretSourceBasicAuthentication] = relationship(
        "SecretSourceBasicAuthentication", back_populates="SecretSource")
    SecretSourceKerberosAuthentications: List[SecretSourceKerberosAuthentication] = relationship(
        "SecretSourceKerberosAuthentication", back_populates="SecretSource")
