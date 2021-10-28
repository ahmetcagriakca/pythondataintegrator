from typing import List

from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from models.dao.base import Base
from models.base.secret.SecretSourceBase import SecretSourceBase
from pdip.data import Entity
from models.dao.secret.SecretSourceBasicAuthentication import SecretSourceBasicAuthentication


class SecretSource(SecretSourceBase, Entity, Base):
    __tablename__ = "SecretSource"
    __table_args__ = {"schema": "Secret"}
    SecretId = Column(Integer, ForeignKey('Secret.Secret.Id'))
    AuthenticationTypeId = Column(Integer, ForeignKey('Secret.AuthenticationType.Id'))
    Secret = relationship("Secret", back_populates="SecretSources")
    AuthenticationType = relationship("AuthenticationType", back_populates="SecretSources")
    SecretSourceBasicAuthentications: List[SecretSourceBasicAuthentication] = relationship(
        "SecretSourceBasicAuthentication", back_populates="SecretSource")