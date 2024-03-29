from pdip.data.domain import Entity
from sqlalchemy import Column, Integer, ForeignKey, Text
from sqlalchemy.orm import relationship

from src.domain.base import Base
from src.domain.base.secret.SecretSourceBasicAuthenticationBase import SecretSourceBasicAuthenticationBase


class SecretSourceBasicAuthentication(SecretSourceBasicAuthenticationBase, Entity, Base):
    __tablename__ = "SecretSourceBasicAuthentication"
    __table_args__ = {"schema": "Secret"}
    SecretSourceId = Column(Integer, ForeignKey('Secret.SecretSource.Id'))
    User = Column(Text, index=False, unique=False, nullable=False)
    Password = Column(Text, index=False, unique=False, nullable=False)
    SecretSource = relationship("SecretSource", back_populates="SecretSourceBasicAuthentications")
