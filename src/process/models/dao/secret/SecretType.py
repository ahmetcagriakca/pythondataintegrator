from typing import List

from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from IocManager import IocManager
from models.base.secret.SecretTypeBase import SecretTypeBase
from models.dao.Entity import Entity
from models.dao.secret.Secret import Secret
from models.dao.secret.AuthenticationType import AuthenticationType


class SecretType(SecretTypeBase,Entity, IocManager.Base):
    __tablename__ = "SecretType"
    __table_args__ = {"schema": "Secret"}
    Name = Column(String(100), index=False, unique=True, nullable=False)
    Secrets: List[Secret] = relationship("Secret", back_populates="SecretType")
    AuthenticationTypes: List[AuthenticationType] = relationship("AuthenticationType", back_populates="SecretType")

    def __init__(*args,**kwargs):
        super().__init__(*args,**kwargs)