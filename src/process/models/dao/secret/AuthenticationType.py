
from typing import List

from models.base.secret.AuthenticationTypeBase import AuthenticationTypeBase
from models.dao.secret.SecretSource import SecretSource
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from IocManager import IocManager
from models.dao.Entity import Entity


class AuthenticationType(AuthenticationTypeBase,Entity, IocManager.Base):
    __tablename__ = "AuthenticationType"
    __table_args__ = {"schema": "Secret"}
    SecretTypeId = Column(Integer, ForeignKey('Secret.SecretType.Id'))
    Name = Column(String(100), index=False, unique=True, nullable=False)
    SecretType = relationship("SecretType", back_populates="AuthenticationTypes")
    SecretSources: List[SecretSource] = relationship("SecretSource", back_populates="AuthenticationType")

    def __init__(*args,**kwargs):
        super().__init__(*args,**kwargs)