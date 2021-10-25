from injector import inject
from sqlalchemy import distinct, func
from sqlalchemy.orm import Query
from pdip.dependency import IScoped
from pdip.data import RepositoryProvider
from models.dao.operation.DataOperationJobExecution import DataOperationJobExecution
from domain.dashboard.GetDataOperationJobExecutionWidget.GetDataOperationJobExecutionWidgetQuery import GetDataOperationJobExecutionWidgetQuery


class GetDataOperationJobExecutionWidgetSpecifications(IScoped):
    @inject
    def __init__(self,
                 repository_provider: RepositoryProvider,
                 ):
        self.repository_provider = repository_provider
        

    def __specified_query(self, query: GetDataOperationJobExecutionWidgetQuery) -> Query:
        specified_query = self.repository_provider.query(
            func.count(distinct(DataOperationJobExecution.Id)).label("Count"),
        )
        return specified_query
        
    def specify(self, query: GetDataOperationJobExecutionWidgetQuery) -> Query:
    
        data_query = self.__specified_query(query=query)
        return data_query

    def count(self, query: GetDataOperationJobExecutionWidgetQuery) -> Query:
        return self.__specified_query(query=query).count()
