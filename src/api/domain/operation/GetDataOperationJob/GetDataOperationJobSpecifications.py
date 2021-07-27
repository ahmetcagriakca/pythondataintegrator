from injector import inject
from sqlalchemy.orm import Query

from infrastructure.data.RepositoryProvider import RepositoryProvider
from infrastructure.dependency.scopes import IScoped
from domain.operation.GetDataOperationJob.GetDataOperationJobQuery import GetDataOperationJobQuery
from models.dao.aps import ApSchedulerJob
from models.dao.operation import DataOperation, DataOperationJob


class GetDataOperationJobSpecifications(IScoped):
    @inject
    def __init__(self,
                 repository_provider: RepositoryProvider):
        self.repository_provider = repository_provider
        pass

    def __specified_query(self, query: GetDataOperationJobQuery) -> Query:
        repository = self.repository_provider.get(DataOperationJob)
        data_query = repository.table
        specified_query = data_query \
            .join(DataOperation) \
            .join(ApSchedulerJob)
        specified_query = specified_query.filter(DataOperationJob.Id == query.request.Id)
        return specified_query

    def specify(self, query: GetDataOperationJobQuery) -> Query:
        data_query = self.__specified_query(query=query)
        return data_query

    def count(self, query: GetDataOperationJobQuery) -> Query:
        return self.__specified_query(query=query).count()
