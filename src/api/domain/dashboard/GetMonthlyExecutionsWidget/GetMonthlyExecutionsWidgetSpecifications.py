from injector import inject
from sqlalchemy.orm import Query
from infrastructure.dependency.scopes import IScoped
from infrastructure.data.RepositoryProvider import RepositoryProvider
from models.dao.operation.DataOperationJobExecution import DataOperationJobExecution
from domain.dashboard.GetMonthlyExecutionsWidget.GetMonthlyExecutionsWidgetQuery import GetMonthlyExecutionsWidgetQuery


class GetMonthlyExecutionsWidgetSpecifications(IScoped):
    @inject
    def __init__(self,
                 repository_provider: RepositoryProvider,
                 ):
        self.repository_provider = repository_provider
        

    def __specified_query(self, query: GetMonthlyExecutionsWidgetQuery) -> Query:
        repository = self.repository_provider.get(DataOperationJobExecution)
        specified_query = repository.table 
        # TODO:specify query
        return specified_query
        
    def specify(self, query: GetMonthlyExecutionsWidgetQuery) -> Query:
    
        data_query = self.__specified_query(query=query)
        return data_query

    def count(self, query: GetMonthlyExecutionsWidgetQuery) -> Query:
        return self.__specified_query(query=query).count()
