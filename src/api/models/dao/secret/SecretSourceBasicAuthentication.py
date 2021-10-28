from sqlalchemy import Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship

from models.dao.base import Base
from pdip.data import Entity


class SecretSourceBasicAuthentication(Entity, Base):
    __tablename__ = "SecretSourceBasicAuthentication"
    __table_args__ = {"schema": "Secret"}
    SecretSourceId = Column(Integer, ForeignKey('Secret.SecretSource.Id'))
    User = Column(String(100), index=False, unique=False, nullable=False)
    Password = Column(String(100), index=False, unique=False, nullable=False)
    SecretSource = relationship("SecretSource", back_populates="SecretSourceBasicAuthentications")

    def __init__(self,
                 SecretSourceId: int = None,
                 User: str = None,
                 Password: str = None,
                 SecretSource = None,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.SecretSourceId: int = SecretSourceId
        self.User: str = User
        self.Password: str = Password
        self.SecretSource = SecretSource
