from typing import List

from pdip.data import Entity
from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from scheduler.domain.base import Base
from scheduler.domain.secret.SecretSourceBasicAuthentication import SecretSourceBasicAuthentication


class SecretSource(Entity, Base):
    __tablename__ = "SecretSource"
    __table_args__ = {"schema": "Secret"}
    SecretId = Column(Integer, ForeignKey('Secret.Secret.Id'))
    AuthenticationTypeId = Column(Integer, ForeignKey('Secret.AuthenticationType.Id'))
    Secret = relationship("Secret", back_populates="SecretSources")
    AuthenticationType = relationship("AuthenticationType", back_populates="SecretSources")
    SecretSourceBasicAuthentications: List[SecretSourceBasicAuthentication] = relationship(
        "SecretSourceBasicAuthentication", back_populates="SecretSource")

    def __init__(self,
                 SecretId: int = None,
                 AuthenticationTypeId: int = None,
                 Secret=None,
                 AuthenticationType=None,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.SecretId: int = SecretId
        self.AuthenticationTypeId: int = AuthenticationTypeId
        self.Secret = Secret
        self.AuthenticationType = AuthenticationType
