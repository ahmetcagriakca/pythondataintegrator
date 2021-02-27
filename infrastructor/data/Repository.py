from typing import Generic, List, TypeVar

from sqlalchemy.dialects.postgresql import psycopg2
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm import Query

from infrastructor.data.DatabaseSessionManager import DatabaseSessionManager
from infrastructor.dependency.scopes import IScoped
from models.dao.Entity import Entity

T = TypeVar('T', bound=Entity)


class Repository(Generic[T], IScoped):
    def __init__(self, database_session_manager: DatabaseSessionManager):
        self.database_session_manager: DatabaseSessionManager = database_session_manager
        self.type = self.__orig_class__.__args__[0]

    def unexpected_error_handler(func):
        def inner(*args, **kwargs):
            # database_session_manager = IocManager.injector.get(DatabaseSessionManager)
            try:
                return func(*args, **kwargs)
            except Exception as ex:
                args[0].database_session_manager.close()
                args[0].database_session_manager.connect()
                print(ex)
                raise

        return inner

    @property
    @unexpected_error_handler
    def table(self):
        return self.database_session_manager.session.query(self.type)

    @unexpected_error_handler
    def insert(self, entity: T):
        self.database_session_manager.session.add(entity)

    @unexpected_error_handler
    def first(self, **kwargs) -> T:
        query: Query = self.table.filter_by(**kwargs)
        return query.first()

    @unexpected_error_handler
    def filter_by(self, **kwargs) -> List[T]:
        query: Query = self.database_session_manager.session.query(self.type)
        return query.filter_by(**kwargs)

    @unexpected_error_handler
    def get(self) -> List[T]:
        query = self.database_session_manager.session.query(self.type)
        return query.all()

    @unexpected_error_handler
    def get_by_id(self, id: int) -> T:
        query = self.database_session_manager.session.query(self.type)
        return query.filter_by(Id=id).first()

    @unexpected_error_handler
    def update(self, id: int, update_entity: T):
        entity = self.get_by_id(id)

    @unexpected_error_handler
    def delete_by_id(self, id: int):
        entity = self.get_by_id(id)
        entity.IsDeleted = 1

    @unexpected_error_handler
    def delete(self, entity: T):
        entity.IsDeleted = 1
