from injector import inject
from sqlalchemy import distinct, func
from sqlalchemy.orm import Query
from pdip.dependency import IScoped
from pdip.data import RepositoryProvider
from models.dao.operation.DataOperationJob import DataOperationJob
from domain.dashboard.GetDataOperationJobWidget.GetDataOperationJobWidgetQuery import GetDataOperationJobWidgetQuery


class GetDataOperationJobWidgetSpecifications(IScoped):
    @inject
    def __init__(self,
                 repository_provider: RepositoryProvider,
                 ):
        self.repository_provider = repository_provider
        

    def __specified_query(self, query: GetDataOperationJobWidgetQuery) -> Query:
        specified_query = self.repository_provider.query(
            func.count(distinct(DataOperationJob.Id)).label("Count"),
        )
        return specified_query
        
    def specify(self, query: GetDataOperationJobWidgetQuery) -> Query:
    
        data_query = self.__specified_query(query=query)
        return data_query

    def count(self, query: GetDataOperationJobWidgetQuery) -> Query:
        return self.__specified_query(query=query).count()
