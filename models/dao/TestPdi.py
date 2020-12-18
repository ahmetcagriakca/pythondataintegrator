from sqlalchemy import Column, String
from infrastructor.IocManager import IocManager
from models.dao.Entity import Entity


class TestPdi(Entity, IocManager.Base):
    __tablename__ = 'TestPdi'
    Code = Column(
        String(100),
        index=True,
        unique=True,
        nullable=False
    )

    def __init__(self, Code: str = None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.Code: str = Code
