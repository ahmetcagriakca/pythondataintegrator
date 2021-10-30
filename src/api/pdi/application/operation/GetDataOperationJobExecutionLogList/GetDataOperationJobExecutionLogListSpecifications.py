from injector import inject
from pdip.data import RepositoryProvider
from pdip.dependency import IScoped
from sqlalchemy.orm import Query

from pdi.application.operation.GetDataOperationJobExecutionLogList.GetDataOperationJobExecutionLogListQuery import \
    GetDataOperationJobExecutionLogListQuery
from pdi.domain.common import Log


class GetDataOperationJobExecutionLogListSpecifications(IScoped):
    @inject
    def __init__(self,
                 repository_provider: RepositoryProvider,
                 ):
        self.repository_provider = repository_provider

    def __specified_query(self, query: GetDataOperationJobExecutionLogListQuery) -> Query:
        repository = self.repository_provider.get(Log)
        specified_query = repository.table.filter_by(JobId=query.request.ExecutionId).order_by(Log.Id)
        return specified_query

    def specify(self, query: GetDataOperationJobExecutionLogListQuery) -> Query:
        data_query = self.__specified_query(query=query)
        return data_query

    def count(self, query: GetDataOperationJobExecutionLogListQuery) -> Query:
        return self.__specified_query(query=query).count()
