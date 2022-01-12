from pdip.data.domain import Entity
from sqlalchemy import Column, Integer, ForeignKey, Text
from sqlalchemy.orm import relationship

from src.domain.base import Base
from src.domain.base.secret.SecretSourceKerberosAuthenticationBase import SecretSourceKerberosAuthenticationBase


class SecretSourceKerberosAuthentication(SecretSourceKerberosAuthenticationBase, Entity, Base):
    __tablename__ = "SecretSourceKerberosAuthentication"
    __table_args__ = {"schema": "Secret"}
    SecretSourceId = Column(Integer, ForeignKey('Secret.SecretSource.Id'))
    Principal = Column(Text, index=False, unique=False, nullable=False)
    Password = Column(Text, index=False, unique=False, nullable=False)
    KrbRealm = Column(Text, index=False, unique=False, nullable=False)
    KrbFqdn = Column(Text, index=False, unique=False, nullable=False)
    KrbServiceName = Column(Text, index=False, unique=False, nullable=False)
    SecretSource = relationship("SecretSource", back_populates="SecretSourceKerberosAuthentications")
