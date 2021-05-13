
from typing import List
from models.dao.secret.SecretSource import SecretSource
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from infrastructor.IocManager import IocManager
from models.dao.Entity import Entity


class AuthenticationType(Entity, IocManager.Base):
    __tablename__ = "AuthenticationType"
    __table_args__ = {"schema": "Secret"}
    SecretTypeId = Column(Integer, ForeignKey('Secret.SecretType.Id'))
    Name = Column(String(100), index=False, unique=True, nullable=False)
    SecretType = relationship("SecretType", back_populates="AuthenticationTypes")

    SecretSources: List[SecretSource] = relationship("SecretSource", back_populates="AuthenticationType")
    def __init__(self,
    
                 SecretTypeId: int = None,
                 Name: str = None,
                 SecretType = None,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.SecretTypeId: int = SecretTypeId
        self.Name: str = Name
        self.SecretType = SecretType
