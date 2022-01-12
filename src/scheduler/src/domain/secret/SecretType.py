from typing import List

from pdip.data.domain import Entity
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship

from src.domain.base import Base
from src.domain.secret.AuthenticationType import AuthenticationType
from src.domain.secret.Secret import Secret


class SecretType(Entity, Base):
    __tablename__ = "SecretType"
    __table_args__ = {"schema": "Secret"}
    Name = Column(String(100), index=False, unique=True, nullable=False)
    Secrets: List[Secret] = relationship("Secret", back_populates="SecretType")
    AuthenticationTypes: List[AuthenticationType] = relationship("AuthenticationType", back_populates="SecretType")

    def __init__(self,
                 Name: int = None,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.Name: int = Name
