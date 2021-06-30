from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship

from IocManager import IocManager
from models.base.secret.SecretSourceBasicAuthenticationBase import SecretSourceBasicAuthenticationBase
from models.dao.Entity import Entity


class SecretSourceBasicAuthentication(SecretSourceBasicAuthenticationBase,Entity, IocManager.Base):
    __tablename__ = "SecretSourceBasicAuthentication"
    __table_args__ = {"schema": "Secret"}
    SecretSourceId = Column(Integer, ForeignKey('Secret.SecretSource.Id'))
    User = Column(String(100), index=False, unique=False, nullable=False)
    Password = Column(String(100), index=False, unique=False, nullable=False)
    SecretSource = relationship("SecretSource", back_populates="SecretSourceBasicAuthentications")