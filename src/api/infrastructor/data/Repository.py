from datetime import datetime
from typing import Generic, List, TypeVar, Optional

from injector import inject
from sqlalchemy.orm import Query

from infrastructor.data.DatabaseSessionManager import DatabaseSessionManager
from models.dao.Entity import Entity

T = TypeVar('T', bound=Entity)


class Repository(Generic[T]):
    @inject
    def __init__(self, database_session_manager: DatabaseSessionManager):
        self.database_session_manager: DatabaseSessionManager = database_session_manager
        self.type = self.__orig_class__.__args__[0]

    @property
    def table(self):
        return self.database_session_manager.session.query(self.type)

    def first(self, **kwargs) -> T:
        query: Query = self.table.filter_by(**kwargs)
        return query.first()

    def filter_by(self, **kwargs) -> List[T]:
        return self.table.filter_by(**kwargs)

    def get(self) -> List[T]:
        return self.table.all()

    def get_by_id(self, id: int) -> T:
        return self.table.filter_by(Id=id).first()

    def insert(self, entity: T):
        self.database_session_manager.session.add(entity)

    def update(self, entity: T):
        entity.LastUpdatedDate = datetime.now()
        entity.LastUpdatedUserId = 0

    def delete_by_id(self, id: int):
        entity = self.get_by_id(id)
        entity.IsDeleted = 1
        entity.LastUpdatedDate = datetime.now()
        entity.LastUpdatedUserId = 0

    def delete(self, entity: T):
        entity.IsDeleted = 1
        entity.LastUpdatedDate = datetime.now()
        entity.LastUpdatedUserId = 0

    def commit(self):
        self.database_session_manager.commit()
