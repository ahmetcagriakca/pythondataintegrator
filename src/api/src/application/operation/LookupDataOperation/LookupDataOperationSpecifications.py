from injector import inject
from pdip.dependency import IScoped
from sqlalchemy import text
from sqlalchemy.orm import Query

from src.application.operation.LookupDataOperation.LookupDataOperationQuery import LookupDataOperationQuery


class LookupDataOperationSpecifications(IScoped):
    @inject
    def __init__(self,
                 ):
        pass

    def __specified_query(self, query: LookupDataOperationQuery, data_query: Query) -> Query:
        specified_query = data_query.order_by(text('"DefinitionId" desc'))
        return specified_query

    def specify(self, data_query: Query, query: LookupDataOperationQuery) -> Query:
        data_query = self.__specified_query(query=query, data_query=data_query)
        return data_query

    def count(self, query: LookupDataOperationQuery, data_query: Query) -> Query:
        return self.__specified_query(query=query, data_query=data_query).count()
