from injector import inject
from pdip.data import RepositoryProvider
from pdip.dependency import IScoped
from sqlalchemy.orm import Query

from domain.common.LookupStatus.LookupStatusQuery import LookupStatusQuery
from models.dao.common import Status


class LookupStatusSpecifications(IScoped):
    @inject
    def __init__(self,
                 repository_provider: RepositoryProvider,
                 ):
        self.repository_provider = repository_provider

    def __specified_query(self, query: LookupStatusQuery) -> Query:
        repository = self.repository_provider.get(Status)
        specified_query = repository.table
        return specified_query

    def specify(self, query: LookupStatusQuery) -> Query:
        data_query = self.__specified_query(query=query)
        return data_query

    def count(self, query: LookupStatusQuery) -> int:
        return self.__specified_query(query=query).count()
