from typing import List

from pdip.data.domain import Entity
from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship

from scheduler.domain.base import Base
from scheduler.domain.secret.SecretSource import SecretSource


class AuthenticationType(Entity, Base):
    __tablename__ = "AuthenticationType"
    __table_args__ = {"schema": "Secret"}
    SecretTypeId = Column(Integer, ForeignKey('Secret.SecretType.Id'))
    Name = Column(String(100), index=False, unique=True, nullable=False)
    SecretType = relationship("SecretType", back_populates="AuthenticationTypes")

    SecretSources: List[SecretSource] = relationship("SecretSource", back_populates="AuthenticationType")

    def __init__(self,

                 SecretTypeId: int = None,
                 Name: str = None,
                 SecretType=None,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.SecretTypeId: int = SecretTypeId
        self.Name: str = Name
        self.SecretType = SecretType
